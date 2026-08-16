#!/bin/zsh

# Validate the NetNewsWire OPML bundle and every direct feed endpoint.
# Usage: ./validate-rss-bundle.sh [path/to/bundle.opml]

set -u
set -o pipefail

script_dir="${0:A:h}"
script_path="${0:A}"
bundle_file="${1:-$script_dir/NetNewsWire-Finance-Cyber.opml}"
source_table_file="${SOURCE_TABLE_FILE:-$script_dir/NetNewsWire-Finance-Cyber-Source-Table.md}"
manifest_file_path="${MANIFEST_FILE:-$script_dir/feed-manifest.json}"
report_markdown_file="${REPORT_MARKDOWN_FILE:-$script_dir/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md}"
report_json_file="${REPORT_JSON_FILE:-$script_dir/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json}"
report_generator="$script_dir/generate-rss-validation-report.py"
validation_profile="${VALIDATION_PROFILE:-master}"
validation_cache_dir="${VALIDATION_CACHE_DIR:-$script_dir/.rss-validation-cache}"
validation_history_file="${VALIDATION_HISTORY_FILE:-$script_dir/.validation-history.json}"

for required_command in curl xmllint python3; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    print -u2 "Required command not found: $required_command"
    exit 2
  fi
done

if [[ ! -f "$bundle_file" ]]; then
  print -u2 "OPML file not found: $bundle_file"
  exit 2
fi

if [[ ! -f "$source_table_file" ]]; then
  print -u2 "Source table not found: $source_table_file"
  exit 2
fi

if [[ ! -f "$manifest_file_path" ]]; then
  print -u2 "Feed manifest not found: $manifest_file_path"
  exit 2
fi

if [[ ! -f "$report_generator" ]]; then
  print -u2 "Report generator not found: $report_generator"
  exit 2
fi

if ! validation_config_line=$(PYTHONPATH="$script_dir${PYTHONPATH:+:$PYTHONPATH}" python3 - "$manifest_file_path" <<'PY'
import sys

from bundle_config import load_manifest, validation_settings

settings = validation_settings(load_manifest(sys.argv[1]))
keys = (
    "max_age_days",
    "duplicate_title_rate_limit",
    "min_items_for_noise",
    "mobile_review_bytes",
    "mobile_large_bytes",
    "mobile_slow_seconds",
    "max_response_bytes",
)
print("\t".join(str(settings[key]) for key in keys))
PY
); then
  print -u2 "Invalid validation configuration in manifest: $manifest_file_path"
  exit 2
fi
IFS=$'\t' read -r max_age_days duplicate_title_rate_limit min_items_for_noise mobile_review_bytes mobile_large_bytes mobile_slow_seconds max_response_bytes <<< "$validation_config_line"

if ! xmllint --nonet --noout "$bundle_file" >/dev/null 2>&1; then
  print -u2 "Invalid OPML: $bundle_file"
  exit 1
fi

mkdir -p "$validation_cache_dir"
validation_lock_dir="${validation_cache_dir}.lock"
if ! mkdir "$validation_lock_dir" 2>/dev/null; then
  existing_pid=''
  [[ -f "$validation_lock_dir/pid" ]] && existing_pid="$(<"$validation_lock_dir/pid")"
  if [[ -n "$existing_pid" ]] && kill -0 "$existing_pid" 2>/dev/null; then
    print -u2 "Another RSS validation is using the shared cache/history: $validation_lock_dir (pid $existing_pid)"
    exit 2
  fi
  print -u2 "Removing stale RSS validation lock: $validation_lock_dir"
  rm -f "$validation_lock_dir/pid"
  if ! rmdir "$validation_lock_dir" 2>/dev/null || ! mkdir "$validation_lock_dir" 2>/dev/null; then
    print -u2 "Could not acquire RSS validation lock: $validation_lock_dir"
    exit 2
  fi
fi
print -r -- "$$" > "$validation_lock_dir/pid"

temp_dir=''
cleanup() {
  if [[ -n "$temp_dir" && -d "$temp_dir" ]]; then
    for temp_file in "$temp_dir"/*.xml(N) "$temp_dir"/*.txt(N) "$temp_dir"/*.tsv(N); do
      rm -f "$temp_file"
    done
    for temp_file in "$temp_dir/report"/*(N); do
      rm -f "$temp_file"
    done
    rmdir "$temp_dir/report" 2>/dev/null || true
    rmdir "$temp_dir" 2>/dev/null || true
  fi
  if [[ -f "$validation_lock_dir/pid" && "$(<"$validation_lock_dir/pid")" == "$$" ]]; then
    rm -f "$validation_lock_dir/pid"
    rmdir "$validation_lock_dir" 2>/dev/null || true
  fi
}
if ! temp_dir=$(mktemp -d -t nnw-rss-validation); then
  print -u2 "Could not create RSS validation temporary directory"
  rm -f "$validation_lock_dir/pid"
  rmdir "$validation_lock_dir" 2>/dev/null || true
  exit 2
fi
trap cleanup EXIT INT TERM

cache_meta_safe() {
  print -r -- "$1" | tr $'\t\r\n' ' '
}

opml_urls_file="$temp_dir/opml-urls.txt"
manifest_file="$temp_dir/manifest.tsv"
field_separator=$'\t'

# Parse OPML with XML so entities such as &amp; in query URLs are unescaped
# before curl receives them. The second field records the explicit freshness
# exception for official/event-driven feeds that may be quiet between releases;
# the third field carries any explicit item-link policy from the manifest.
PYTHONPATH="$script_dir${PYTHONPATH:+:$PYTHONPATH}" python3 - "$bundle_file" "$opml_urls_file" <<'PY'
import sys

from rss_validation import safe_xml_root

source, destination = sys.argv[1:]
root = safe_xml_root(source)
urls = []
for outline in root.iter():
    url = (outline.attrib.get("xmlUrl") or "").strip()
    if url:
        event_driven = (outline.attrib.get("eventDriven") or "").strip().lower() == "true"
        item_link_policy = (outline.attrib.get("itemLinkPolicy") or "default").strip().lower()
        urls.append((url, "event-driven" if event_driven else "standard", item_link_policy))

with open(destination, "w", encoding="utf-8") as handle:
    for url, freshness_policy, item_link_policy in urls:
        handle.write(f"{url}\t{freshness_policy}\t{item_link_policy}\n")

if not urls:
    raise SystemExit("OPML contains no xmlUrl feed elements")
PY

total=0
passed=0
failed=0
structured_alert_exceptions=0

while IFS=$'\t' read -r feed_url freshness_policy item_link_policy; do
  freshness_policy="${freshness_policy:-standard}"
  item_link_policy="${item_link_policy:-default}"
  total=$((total + 1))
  feed_file="$temp_dir/feed-$total.xml"
  headers_file="$temp_dir/headers-$total.txt"
  cache_key=$(python3 "$script_dir/rss_validation.py" cache-key "$feed_url")
  cache_body="$validation_cache_dir/$cache_key.xml"
  cache_meta="$validation_cache_dir/$cache_key.meta"
  cached_url=''
  cached_etag=''
  cached_last_modified=''
  cached_content_type=''
  cached_content_encoding=''
  cached_effective_url=''
  if [[ -f "$cache_meta" && -s "$cache_body" ]]; then
    cached_url=$(awk -F '\t' '{print $1}' "$cache_meta")
    cached_etag=$(awk -F '\t' '{print $2}' "$cache_meta")
    cached_last_modified=$(awk -F '\t' '{print $3}' "$cache_meta")
    cached_content_type=$(awk -F '\t' '{print $4}' "$cache_meta")
    cached_content_encoding=$(awk -F '\t' '{print $5}' "$cache_meta")
    cached_effective_url=$(awk -F '\t' '{print $6}' "$cache_meta")
  fi
  curl_headers=()
  if [[ "$cached_url" == "$feed_url" ]]; then
    [[ -n "$cached_etag" ]] && curl_headers+=(-H "If-None-Match: $cached_etag")
    [[ -n "$cached_last_modified" ]] && curl_headers+=(-H "If-Modified-Since: $cached_last_modified")
  fi
  curl_metadata=$(curl -L --proto '=https' --proto-redir '=https' --compressed -sS \
    --connect-timeout 10 --max-time 25 --retry 2 --retry-delay 1 --retry-max-time 60 \
    --max-filesize "$max_response_bytes" \
    -H 'Accept: application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8' \
    -A 'NetNewsWire RSS validation' \
    "${curl_headers[@]}" \
    -D "$headers_file" \
    -o "$feed_file" \
    -w $'%{http_code}\t%{url_effective}\t%{size_download}\t%{time_total}' \
    "$feed_url" 2>/dev/null || true)
  http_code="${curl_metadata%%$'\t'*}"
  metadata_rest="${curl_metadata#*$'\t'}"
  effective_url="${metadata_rest%%$'\t'*}"
  metadata_rest="${metadata_rest#*$'\t'}"
  wire_bytes="${metadata_rest%%$'\t'*}"
  transfer_seconds="${metadata_rest#*$'\t'}"
  [[ "$effective_url" == "$metadata_rest" ]] && effective_url=''
  [[ -n "$http_code" ]] || http_code='000'
  [[ -n "$wire_bytes" && "$wire_bytes" != "$metadata_rest" ]] || wire_bytes='0'
  [[ -n "$transfer_seconds" && "$transfer_seconds" != "$wire_bytes" ]] || transfer_seconds='0'
  not_modified='no'
  cache_hit='no'
  if [[ "$http_code" == '304' && "$cached_url" == "$feed_url" && -s "$cache_body" ]]; then
    cp "$cache_body" "$feed_file"
    not_modified='yes'
    cache_hit='yes'
  fi
  payload_bytes=$(wc -c < "$feed_file" 2>/dev/null | tr -d ' ' || print 0)
  response_size_status='within-limit'
  if (( payload_bytes > max_response_bytes )); then
    response_size_status='too-large'
    rm -f "$feed_file"
    payload_bytes=0
  fi
  content_type=$(awk -F': *' 'tolower($1)=="content-type" {value=$2} END {gsub(/\r/, "", value); print value}' "$headers_file" 2>/dev/null)
  etag=$(awk -F': *' 'tolower($1)=="etag" {value=$2} END {gsub(/\r/, "", value); print value}' "$headers_file" 2>/dev/null)
  last_modified=$(awk -F': *' 'tolower($1)=="last-modified" {value=$2} END {gsub(/\r/, "", value); print value}' "$headers_file" 2>/dev/null)
  content_encoding=$(awk -F': *' 'tolower($1)=="content-encoding" {value=$2} END {gsub(/\r/, "", value); print value}' "$headers_file" 2>/dev/null)
  [[ -n "$content_type" ]] || content_type="$cached_content_type"
  [[ -n "$content_encoding" ]] || content_encoding="$cached_content_encoding"
  [[ -n "$effective_url" ]] || effective_url="$cached_effective_url"
  [[ -n "$etag" ]] || etag="$cached_etag"
  [[ -n "$last_modified" ]] || last_modified="$cached_last_modified"
  content_type_status='safe'
  case "${content_type:l}" in
    *application/json*|*text/json*) content_type_status='rejected' ;;
    *text/html*) content_type_status='mislabelled-xml' ;;
  esac

  feed_root=$(xmllint --nonet --xpath 'name(/*)' "$feed_file" 2>/dev/null)
  secure_transport='no'
  [[ "$feed_url" == https://* ]] && secure_transport='yes'
  effective_secure_transport='no'
  [[ "$effective_url" == https://* ]] && effective_secure_transport='yes'
  feed_title=$(xmllint --nonet --xpath \
    'normalize-space(string((/*[local-name()="rss"]/*[local-name()="channel"]/*[local-name()="title"] | /*[local-name()="feed"]/*[local-name()="title"] | /*[local-name()="RDF"]/*[local-name()="channel"]/*[local-name()="title"])[1]))' \
    "$feed_file" 2>/dev/null)
  item_link=$(xmllint --nonet --xpath \
    'normalize-space(string((//*[local-name()="item"]/*[local-name()="link"][1] | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="link"][@href][1]/@href)[1]))' \
    "$feed_file" 2>/dev/null)
  item_title=$(xmllint --nonet --xpath \
    'normalize-space(string((//*[local-name()="item"][1]/*[local-name()="title"] | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="title"])[1]))' \
    "$feed_file" 2>/dev/null)
  feed_inspection=$(python3 "$script_dir/rss_validation.py" inspect "$feed_file" 2>/dev/null || true)
  latest_date="${feed_inspection%%$'\t'*}"
  inspection_rest="${feed_inspection#*$'\t'}"
  parse_seconds="${inspection_rest%%$'\t'*}"
  [[ "$latest_date" == "$feed_inspection" ]] && latest_date=''
  [[ -n "$parse_seconds" && "$parse_seconds" != "$inspection_rest" ]] || parse_seconds='0'
  age_days=$(python3 "$script_dir/rss_validation.py" age-days "$latest_date" 2>/dev/null || true)
  recent_content='no'
  if [[ -n "$age_days" ]]; then
    recent_content=$(python3 - "$age_days" "$max_age_days" "$freshness_policy" <<'PY' 2>/dev/null || true
import sys
age = float(sys.argv[1])
limit = float(sys.argv[2])
policy = sys.argv[3]
if age < -2:
    print('no')
elif age <= limit:
    print('yes')
elif policy == 'event-driven':
    print('event-driven')
else:
    print('no')
PY
    )
  fi
  valid_item_link='no'
  [[ "$item_link" == http://* || "$item_link" == https://* ]] && valid_item_link='yes'
  # Nasdaq's trade-halt RSS is a structured alert stream: its entries have
  # halt fields and a title but intentionally do not expose per-item URLs.
  if [[ "$valid_item_link" == 'no' && "$item_link_policy" == 'structured-alert' && -n "$item_title" ]]; then
    valid_item_link='structured-alert'
    structured_alert_exceptions=$((structured_alert_exceptions + 1))
  fi

  if [[ "$http_code" == '200' && -s "$feed_file" && ( "$feed_root" == 'rss' || "$feed_root" == 'feed' || "$feed_root" == 'rdf:RDF' || "$feed_root" == 'RDF' ) ]] && xmllint --nonet --noout "$feed_file" >/dev/null 2>&1; then
    cp "$feed_file" "$cache_body"
    print -r -- "$(cache_meta_safe "$feed_url")${field_separator}$(cache_meta_safe "$etag")${field_separator}$(cache_meta_safe "$last_modified")${field_separator}$(cache_meta_safe "$content_type")${field_separator}$(cache_meta_safe "$content_encoding")${field_separator}$(cache_meta_safe "$effective_url")" > "$cache_meta"
  fi

  passed_flag='no'
  if [[ ( "$http_code" == '200' || "$cache_hit" == 'yes' ) ]] && xmllint --nonet --noout "$feed_file" >/dev/null 2>&1 \
    && [[ "$secure_transport" == 'yes' ]] \
    && [[ "$effective_secure_transport" == 'yes' ]] \
    && [[ "$content_type_status" == 'safe' || "$content_type_status" == 'mislabelled-xml' ]] \
    && [[ "$feed_root" == 'rss' || "$feed_root" == 'feed' || "$feed_root" == 'rdf:RDF' || "$feed_root" == 'RDF' ]] \
    && [[ -n "$feed_title" ]] \
    && [[ "$valid_item_link" == 'yes' || "$valid_item_link" == 'structured-alert' ]] \
    && [[ "$recent_content" == 'yes' || "$recent_content" == 'event-driven' ]]; then
    passed=$((passed + 1))
    passed_flag='yes'
    print "OK    $feed_url    root=$feed_root    https=yes    final_https=yes    content_type=$content_type_status    freshness=$freshness_policy    item_link=$valid_item_link    age_days=$age_days    recent=$recent_content    latest=$latest_date"
  else
    failed=$((failed + 1))
    print "FAIL  $feed_url    http=$http_code    root=${feed_root:-unavailable}    https=$secure_transport    final_https=$effective_secure_transport    content_type=$content_type_status    freshness=$freshness_policy    title=$([[ -n "$feed_title" ]] && print yes || print no)    item_link=$valid_item_link    age_days=${age_days:-unavailable}    recent=${recent_content:-no}    latest=${latest_date:-unavailable}"
  fi

  print -r -- "${total}${field_separator}${feed_url}${field_separator}${feed_file}${field_separator}${http_code}${field_separator}${effective_url}${field_separator}${secure_transport}${field_separator}${feed_root}${field_separator}${freshness_policy}${field_separator}${valid_item_link}${field_separator}${recent_content}${field_separator}${age_days}${field_separator}${latest_date}${field_separator}${passed_flag}${field_separator}${content_type}${field_separator}${etag}${field_separator}${last_modified}${field_separator}${payload_bytes}${field_separator}${transfer_seconds}${field_separator}${wire_bytes}${field_separator}${content_encoding}${field_separator}${parse_seconds}${field_separator}${not_modified}${field_separator}${response_size_status}" >> "$manifest_file"
done < "$opml_urls_file"

report_status=0
report_candidate_dir="$temp_dir/report"
mkdir -p "$report_candidate_dir"
# Use the final output basenames even while writing into the temporary
# directory, so the Markdown report's machine-readable link survives the move.
report_candidate_markdown="$report_candidate_dir/${report_markdown_file:t}"
report_candidate_json="$report_candidate_dir/${report_json_file:t}"
python3 "$report_generator" \
  "$bundle_file" \
  "$source_table_file" \
  "$manifest_file" \
  "$report_candidate_markdown" \
  "$report_candidate_json" \
  "$max_age_days" \
  "$duplicate_title_rate_limit" \
  "$min_items_for_noise" \
  "$script_path" \
  "$manifest_file_path" \
  "$validation_profile" \
  "$validation_history_file" || report_status=$?

report_ready='no'
if [[ -s "$report_candidate_markdown" && -s "$report_candidate_json" ]]; then
  mv "$report_candidate_markdown" "$report_markdown_file"
  mv "$report_candidate_json" "$report_json_file"
  report_ready='yes'
else
  print -u2 "Validation report generation did not produce a complete current report; preserving the previous report files."
  [[ "$report_status" == '0' ]] && report_status=2
fi

record_status=0
if [[ "$report_ready" == 'yes' ]]; then
  python3 "$script_dir/record-validation-result.py" \
    --report "$report_json_file" \
    --history "$validation_history_file" \
    --profile "$validation_profile" \
    --current-run \
    --healthy "$([[ "$report_status" == '0' ]] && print yes || print no)" || record_status=$?
else
  record_status=2
fi

print "summary profile=$validation_profile total=$total passed=$passed failed=$failed structured_alert_exceptions=$structured_alert_exceptions max_age_days=$max_age_days max_response_bytes=$max_response_bytes"
(( failed == 0 && report_status == 0 && record_status == 0 ))
