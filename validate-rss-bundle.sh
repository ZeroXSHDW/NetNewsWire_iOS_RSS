#!/bin/zsh

# Validate the NetNewsWire OPML bundle and every direct feed endpoint.
# Usage: ./validate-rss-bundle.sh [path/to/bundle.opml]

set -u

script_dir="${0:A:h}"
script_path="${0:A}"
bundle_file="${1:-$script_dir/NetNewsWire-Finance-Cyber.opml}"
source_table_file="${SOURCE_TABLE_FILE:-$script_dir/NetNewsWire-Finance-Cyber-Source-Table.md}"
manifest_file_path="${MANIFEST_FILE:-$script_dir/feed-manifest.json}"
report_markdown_file="${REPORT_MARKDOWN_FILE:-$script_dir/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md}"
report_json_file="${REPORT_JSON_FILE:-$script_dir/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json}"
report_generator="$script_dir/generate-rss-validation-report.py"
max_age_days="${MAX_AGE_DAYS:-180}"
duplicate_title_rate_limit="${DUPLICATE_TITLE_RATE_LIMIT:-0.50}"
min_items_for_noise="${MIN_ITEMS_FOR_NOISE:-10}"
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

if ! xmllint --noout "$bundle_file" >/dev/null 2>&1; then
  print -u2 "Invalid OPML: $bundle_file"
  exit 1
fi

mkdir -p "$validation_cache_dir"

temp_dir=$(mktemp -d -t nnw-rss-validation)
cleanup() {
  for temp_file in "$temp_dir"/*.xml(N) "$temp_dir"/*.txt(N) "$temp_dir"/*.tsv(N); do
    rm -f "$temp_file"
  done
  rmdir "$temp_dir" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

opml_urls_file="$temp_dir/opml-urls.txt"
manifest_file="$temp_dir/manifest.tsv"
field_separator=$'\t'

# Parse OPML with XML so entities such as &amp; in query URLs are unescaped
# before curl receives them. The second field records the explicit freshness
# exception for official/event-driven feeds that may be quiet between releases.
python3 - "$bundle_file" "$opml_urls_file" <<'PY'
import sys
import xml.etree.ElementTree as ET

source, destination = sys.argv[1:]
root = ET.parse(source).getroot()
urls = []
for outline in root.iter():
    url = (outline.attrib.get("xmlUrl") or "").strip()
    if url:
        event_driven = (outline.attrib.get("eventDriven") or "").strip().lower() == "true"
        urls.append((url, "event-driven" if event_driven else "standard"))

with open(destination, "w", encoding="utf-8") as handle:
    for url, freshness_policy in urls:
        handle.write(f"{url}\t{freshness_policy}\n")

if not urls:
    raise SystemExit("OPML contains no xmlUrl feed elements")
PY

total=0
passed=0
failed=0
structured_alert_exceptions=0

while IFS=$'\t' read -r feed_url freshness_policy; do
  freshness_policy="${freshness_policy:-standard}"
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
  curl_metadata=$(curl -L --compressed -sS --max-time 25 \
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

  feed_root=$(xmllint --xpath 'name(/*)' "$feed_file" 2>/dev/null)
  secure_transport='no'
  [[ "$feed_url" == https://* ]] && secure_transport='yes'
  effective_secure_transport='no'
  [[ "$effective_url" == https://* ]] && effective_secure_transport='yes'
  feed_title=$(xmllint --xpath \
    'normalize-space(string((/*[local-name()="rss"]/*[local-name()="channel"]/*[local-name()="title"] | /*[local-name()="feed"]/*[local-name()="title"] | /*[local-name()="RDF"]/*[local-name()="channel"]/*[local-name()="title"])[1]))' \
    "$feed_file" 2>/dev/null)
  item_link=$(xmllint --xpath \
    'normalize-space(string((//*[local-name()="item"]/*[local-name()="link"][1] | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="link"][@href][1]/@href)[1]))' \
    "$feed_file" 2>/dev/null)
  item_title=$(xmllint --xpath \
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
  if [[ "$valid_item_link" == 'no' && "$feed_url" == 'https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts' && -n "$item_title" ]]; then
    valid_item_link='structured-alert'
    structured_alert_exceptions=$((structured_alert_exceptions + 1))
  fi

  if [[ "$http_code" == '200' && -s "$feed_file" && ( "$feed_root" == 'rss' || "$feed_root" == 'feed' || "$feed_root" == 'rdf:RDF' || "$feed_root" == 'RDF' ) ]] && xmllint --noout "$feed_file" >/dev/null 2>&1; then
    cp "$feed_file" "$cache_body"
    print -r -- "${feed_url}${field_separator}${etag}${field_separator}${last_modified}${field_separator}${content_type}${field_separator}${content_encoding}${field_separator}${effective_url}" > "$cache_meta"
  fi

  passed_flag='no'
  if [[ ( "$http_code" == '200' || "$cache_hit" == 'yes' ) ]] && xmllint --noout "$feed_file" >/dev/null 2>&1 \
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

  print -r -- "${total}${field_separator}${feed_url}${field_separator}${feed_file}${field_separator}${http_code}${field_separator}${effective_url}${field_separator}${secure_transport}${field_separator}${feed_root}${field_separator}${freshness_policy}${field_separator}${valid_item_link}${field_separator}${recent_content}${field_separator}${age_days}${field_separator}${latest_date}${field_separator}${passed_flag}${field_separator}${content_type}${field_separator}${etag}${field_separator}${last_modified}${field_separator}${payload_bytes}${field_separator}${transfer_seconds}${field_separator}${wire_bytes}${field_separator}${content_encoding}${field_separator}${parse_seconds}${field_separator}${not_modified}" >> "$manifest_file"
done < "$opml_urls_file"

report_status=0
python3 "$report_generator" \
  "$bundle_file" \
  "$source_table_file" \
  "$manifest_file" \
  "$report_markdown_file" \
  "$report_json_file" \
  "$max_age_days" \
  "$duplicate_title_rate_limit" \
  "$min_items_for_noise" \
  "$script_path" \
  "$manifest_file_path" \
  "$validation_profile" || report_status=$?

python3 "$script_dir/record-validation-result.py" \
  --report "$report_json_file" \
  --history "$validation_history_file" \
  --profile "$validation_profile" \
  --healthy "$([[ "$report_status" == '0' ]] && print yes || print no)" || true

print "summary profile=$validation_profile total=$total passed=$passed failed=$failed structured_alert_exceptions=$structured_alert_exceptions max_age_days=$max_age_days"
(( failed == 0 && report_status == 0 ))
