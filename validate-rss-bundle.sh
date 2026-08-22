#!/bin/zsh

# Validate the NetNewsWire OPML bundle and every direct feed endpoint.
# Usage: ./validate-rss-bundle.sh [path/to/bundle.opml]

set -u
set -o pipefail

script_dir="${0:A:h}"
script_path="${0:A}"
bundle_file="${1:-$script_dir/artifacts/opml/NetNewsWire-Finance-Cyber.opml}"
source_table_file="${SOURCE_TABLE_FILE:-$script_dir/artifacts/sources/NetNewsWire-Finance-Cyber-Source-Table.md}"
manifest_file_path="${MANIFEST_FILE:-$script_dir/feed-manifest.json}"
report_markdown_file="${REPORT_MARKDOWN_FILE:-$script_dir/artifacts/validation/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md}"
report_json_file="${REPORT_JSON_FILE:-$script_dir/artifacts/validation/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json}"
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
# before curl receives them. The second field records the freshness policy, the
# third carries any explicit item-link policy, and the fourth is the stable
# manifest/OPML display title used when a publisher omits its channel title.
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
        display_title = (outline.attrib.get("title") or outline.attrib.get("text") or "").strip()
        urls.append((url, "event-driven" if event_driven else "standard", item_link_policy, display_title))

with open(destination, "w", encoding="utf-8") as handle:
    for url, freshness_policy, item_link_policy, display_title in urls:
        handle.write(f"{url}\t{freshness_policy}\t{item_link_policy}\t{display_title}\n")

if not urls:
    raise SystemExit("OPML contains no xmlUrl feed elements")
PY

total=0
passed=0
failed=0
structured_alert_exceptions=0

while IFS=$'\t' read -r feed_url freshness_policy item_link_policy manifest_title; do
  freshness_policy="${freshness_policy:-standard}"
  item_link_policy="${item_link_policy:-default}"
  manifest_title="${manifest_title:-}"
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
    # Ignore truncated legacy cache metadata; a malformed conditional header
    # can make an otherwise healthy publisher return an HTTP-000 transport
    # failure.  Valid HTTP dates include the weekday comma, time colons and
    # the GMT suffix.
    [[ "$cached_last_modified" == *,*:*:*\ GMT ]] && curl_headers+=(-H "If-Modified-Since: $cached_last_modified")
  fi
  curl_user_agent=(-A 'NetNewsWire RSS validation')
  curl_http_version=()
  curl_accept=(-H 'Accept: application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8')
  # The European Parliament RSS host returns an HTTP 202 challenge page to
  # synthetic validator identities, while its normal public response is RSS.
  # The Reserve Bank of Australia and Dutch central-bank RSS hosts similarly
  # block descriptive user-agent strings with their WAFs; neutral/default curl
  # identities return valid XML. The NRC RSS endpoint applies the same policy.
  # FEMA's RSS host currently returns 403 for descriptive identities but serves
  # the same official feeds to the neutral/default curl identity. The European
  # Environment Agency's XML cache intermittently times out for the descriptive
  # identity while serving the same official feeds to the neutral/default one.
  # The St. Louis Fed RSS host additionally needs HTTP/1.1; its official feeds
  # return a valid XML response to the neutral HTTP/1.1 curl transport but can
  # fail with an HTTP/2 INTERNAL_ERROR under the descriptive validator request.
  # African Development Bank's Cloudflare layer can return one intermittent
  # HTTP 403 for the default HTTP/2 transport while serving the same feed over
  # HTTP/1.1. Keep that transport choice endpoint-scoped; it does not weaken
  # the XML, HTTPS or freshness gates below.
  # Leave the established identity in place for every other feed.
  if [[ "$feed_url" == 'https://www.europarl.europa.eu/rss/doc/press-releases-committees/en.xml' ]] \
    || [[ "$feed_url" == 'https://www.europarl.europa.eu/rss/doc/press-releases-plenary/en.xml' ]] \
    || [[ "$feed_url" == https://www.rba.gov.au/rss/* ]] \
    || [[ "$feed_url" == https://www.dnb.nl/en/rss/* ]] \
    || [[ "$feed_url" == 'https://www.consumerfinance.gov/about-us/newsroom/feed/' ]] \
    || [[ "$feed_url" == https://www.nrc.gov/public-involve/rss\?feed=* ]] \
    || [[ "$feed_url" == https://www.fema.gov/feeds/* ]] \
    || [[ "$feed_url" == https://www.eea.europa.eu/en/newsroom/rss-feeds/*/rss.xml ]] \
    || [[ "$feed_url" == https://www.stlouisfed.org/rss/* ]]; then
    curl_user_agent=()
  fi
  # Eurostat's catalogue API returns HTTP 406 when an RSS-specific Accept
  # header is sent, but serves the same official RSS/XML document with the
  # default curl Accept behavior. Keep this exception endpoint-scoped.
  if [[ "$feed_url" == https://ec.europa.eu/eurostat/api/dissemination/catalogue/rss/* ]]; then
    curl_accept=()
  fi
  if [[ "$feed_url" == https://www.stlouisfed.org/rss/* ]] \
    || [[ "$feed_url" == 'https://www.afdb.org/en/news-and-events/rss' ]]; then
    curl_http_version=(--http1.1)
  fi
  curl_failure_options=()
  curl_extra_headers=()
  if [[ "$feed_url" == 'https://www.afdb.org/en/news-and-events/rss' ]]; then
    curl_failure_options=(--fail-with-body --retry-all-errors)
    curl_extra_headers=(-H 'Referer: https://www.afdb.org/en/rss-feeds')
  fi
  curl_compression=(--compressed)
  # The Swedish Riksbank currently sends a valid XML body with the invalid
  # Content-Encoding value `System.Text.UTF8Encoding+UTF8EncodingSealed`.
  # Do not ask curl to decode that response; the uncompressed body remains a
  # reproducible RSS response and is what NetNewsWire can consume.
  if [[ "$feed_url" == https://www.riksbank.se/sv/rss/* ]]; then
    curl_compression=()
  fi
  curl_metadata=$(curl -L --proto '=https' --proto-redir '=https' -sS \
    --connect-timeout 10 --max-time 25 --retry 2 --retry-delay 1 --retry-max-time 60 \
    --max-filesize "$max_response_bytes" \
    "${curl_failure_options[@]}" \
    "${curl_extra_headers[@]}" \
    "${curl_accept[@]}" \
    "${curl_compression[@]}" \
    "${curl_http_version[@]}" \
    "${curl_user_agent[@]}" \
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
  # Split response headers at their first colon only.  Last-Modified values
  # contain a time colon; using `-F': *'` truncates those validators and can
  # make the next conditional request look malformed to the publisher.
  content_type=$(awk 'tolower($1)=="content-type" {value=substr($0, index($0, ":") + 1)} END {gsub(/^[[:space:]]+|[[:space:]]*\r$/, "", value); print value}' "$headers_file" 2>/dev/null)
  etag=$(awk 'tolower($1)=="etag" {value=substr($0, index($0, ":") + 1)} END {gsub(/^[[:space:]]+|[[:space:]]*\r$/, "", value); print value}' "$headers_file" 2>/dev/null)
  last_modified=$(awk 'tolower($1)=="last-modified" {value=substr($0, index($0, ":") + 1)} END {gsub(/^[[:space:]]+|[[:space:]]*\r$/, "", value); print value}' "$headers_file" 2>/dev/null)
  content_encoding=$(awk 'tolower($1)=="content-encoding" {value=substr($0, index($0, ":") + 1)} END {gsub(/^[[:space:]]+|[[:space:]]*\r$/, "", value); print value}' "$headers_file" 2>/dev/null)
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
    'normalize-space(string((//*[local-name()="item"]/*[local-name()="link"][normalize-space(.)][1] | /*[local-name()="item"]/*[local-name()="link"][@href][1]/@href | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="link"][@href][1]/@href | /*[local-name()="rss"]//*[local-name()="item"][1]/*[local-name()="guid"][starts-with(normalize-space(.), "http://") or starts-with(normalize-space(.), "https://")][1] | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="guid"][starts-with(normalize-space(.), "http://") or starts-with(normalize-space(.), "https://")][1])[1]))' \
    "$feed_file" 2>/dev/null)
  item_title=$(xmllint --nonet --xpath \
    'normalize-space(string((//*[local-name()="item"][1]/*[local-name()="title"] | /*[local-name()="feed"]//*[local-name()="entry"][1]/*[local-name()="title"])[1]))' \
    "$feed_file" 2>/dev/null)
  xml_valid='no'
  if xmllint --nonet --noout "$feed_file" >/dev/null 2>&1; then
    xml_valid='yes'
  else
    # libxml2/xmllint rejects some otherwise safe feeds when one CDATA
    # section exceeds its parser limit. Fall back to the shared Python
    # parser, which rejects DTD/entity declarations and enforces its own
    # bounded XML size before extracting the same feed metadata.
    python_xml_metadata=$(PYTHONPATH="$script_dir${PYTHONPATH:+:$PYTHONPATH}" python3 - "$feed_file" <<'PY' 2>/dev/null || true
import sys

from rss_validation import extract_feed, local_name, safe_xml_root

root = safe_xml_root(sys.argv[1])
feed_title, items = extract_feed(root)
first_item = items[0] if items else {}
print(
    "\t".join(
        [
            local_name(root.tag),
            feed_title,
            str(first_item.get("link") or ""),
            str(first_item.get("title") or ""),
        ]
    )
)
PY
    )
    if [[ -n "$python_xml_metadata" ]]; then
      IFS=$'\t' read -r fallback_root fallback_title fallback_item_link fallback_item_title <<< "$python_xml_metadata"
      [[ -n "$feed_root" ]] || feed_root="$fallback_root"
      [[ -n "$feed_title" ]] || feed_title="$fallback_title"
      [[ -n "$item_link" ]] || item_link="$fallback_item_link"
      [[ -n "$item_title" ]] || item_title="$fallback_item_title"
      xml_valid='yes'
    fi
  fi
  # A few official RSS feeds publish valid relative article paths. Resolve
  # those against the verified HTTPS feed URL before applying the transport
  # gate; the shared Python report parser already uses the same rule.
  if [[ "$xml_valid" == 'yes' ]] \
    && [[ "$item_link" != http://* && "$item_link" != https://* ]]; then
    python_xml_metadata=$(PYTHONPATH="$script_dir${PYTHONPATH:+:$PYTHONPATH}" python3 - "$feed_file" "$effective_url" <<'PY' 2>/dev/null || true
import sys

from rss_validation import extract_feed, local_name, safe_xml_root

root = safe_xml_root(sys.argv[1])
feed_title, items = extract_feed(root, base_url=sys.argv[2])
first_item = items[0] if items else {}
print(
    "\t".join(
        [
            local_name(root.tag),
            feed_title,
            str(first_item.get("link") or ""),
            str(first_item.get("title") or ""),
        ]
    )
)
PY
    )
    if [[ -n "$python_xml_metadata" ]]; then
      IFS=$'\t' read -r fallback_root fallback_title fallback_item_link fallback_item_title <<< "$python_xml_metadata"
      [[ -n "$feed_root" ]] || feed_root="$fallback_root"
      [[ -n "$feed_title" ]] || feed_title="$fallback_title"
      [[ -z "$fallback_item_link" ]] || item_link="$fallback_item_link"
      [[ -n "$item_title" ]] || item_title="$fallback_item_title"
    fi
  fi
  # Some otherwise valid official feeds omit the channel title. Use the
  # manifest-authored display title so NetNewsWire and the validator retain a
  # stable identity while still requiring every item title/date/link to pass.
  [[ -n "$feed_title" ]] || feed_title="$manifest_title"
  feed_inspection=$(python3 "$script_dir/rss_validation.py" inspect "$feed_file" 2>/dev/null || true)
  latest_date="${feed_inspection%%$'\t'*}"
  inspection_rest="${feed_inspection#*$'\t'}"
  parse_seconds="${inspection_rest%%$'\t'*}"
  [[ "$latest_date" == "$feed_inspection" ]] && latest_date=''
  [[ -n "$parse_seconds" && "$parse_seconds" != "$inspection_rest" ]] || parse_seconds='0'
  item_count=$(PYTHONPATH="$script_dir${PYTHONPATH:+:$PYTHONPATH}" python3 - "$feed_file" <<'PY' 2>/dev/null || true
import sys

from rss_validation import extract_feed, safe_xml_root

root = safe_xml_root(sys.argv[1])
_, items = extract_feed(root)
print(len(items))
PY
  )
  [[ "$item_count" =~ ^[0-9]+$ ]] || item_count=''
  age_days=$(python3 "$script_dir/rss_validation.py" age-days "$latest_date" 2>/dev/null || true)
  recent_content='no'
  if [[ -n "$age_days" ]]; then
    recent_content=$(python3 - "$age_days" "$max_age_days" "$freshness_policy" <<'PY' 2>/dev/null || true
import sys
age = float(sys.argv[1])
limit = float(sys.argv[2])
policy = sys.argv[3]
if age < -2:
    print('event-driven' if policy == 'event-driven' else 'no')
elif age <= limit:
    print('yes')
elif policy == 'event-driven':
    print('event-driven')
else:
    print('no')
PY
    )
  elif [[ "$freshness_policy" == 'event-driven' && "$item_count" == '0' ]]; then
    # A healthy operational-alert feed can be empty when there is no active
    # incident. Keep this distinct from a stale feed so the report and drift
    # checks describe the no-event state accurately.
    recent_content='event-driven-empty'
  fi
  valid_item_link='no'
  [[ "$item_link" == http://* || "$item_link" == https://* ]] && valid_item_link='yes'
  if [[ "$freshness_policy" == 'event-driven' && "$item_count" == '0' ]]; then
    valid_item_link='event-driven-empty'
  fi
  # Explicit structured-alert feeds may have valid links but repeated
  # identifier/state titles that are the alert payload itself. Treat the
  # manifest policy as authoritative for the noise gate; it also covers the
  # existing Nasdaq halt stream whose entries intentionally lack URLs.
  if [[ "$item_link_policy" == 'structured-alert' && -n "$item_title" ]]; then
    valid_item_link='structured-alert'
    structured_alert_exceptions=$((structured_alert_exceptions + 1))
  fi

  if [[ "$http_code" == '200' && -s "$feed_file" && "$xml_valid" == 'yes' && ( "$feed_root" == 'rss' || "$feed_root" == 'feed' || "$feed_root" == 'rdf:RDF' || "$feed_root" == 'RDF' ) ]]; then
    cp "$feed_file" "$cache_body"
    print -r -- "$(cache_meta_safe "$feed_url")${field_separator}$(cache_meta_safe "$etag")${field_separator}$(cache_meta_safe "$last_modified")${field_separator}$(cache_meta_safe "$content_type")${field_separator}$(cache_meta_safe "$content_encoding")${field_separator}$(cache_meta_safe "$effective_url")" > "$cache_meta"
  fi

  passed_flag='no'
  if [[ ( "$http_code" == '200' || "$cache_hit" == 'yes' ) ]] && [[ "$xml_valid" == 'yes' ]] \
    && [[ "$secure_transport" == 'yes' ]] \
    && [[ "$effective_secure_transport" == 'yes' ]] \
    && [[ "$content_type_status" == 'safe' || "$content_type_status" == 'mislabelled-xml' ]] \
    && [[ "$feed_root" == 'rss' || "$feed_root" == 'feed' || "$feed_root" == 'rdf:RDF' || "$feed_root" == 'RDF' ]] \
    && [[ -n "$feed_title" ]] \
    && [[ "$valid_item_link" == 'yes' || "$valid_item_link" == 'structured-alert' || "$valid_item_link" == 'event-driven-empty' ]] \
    && [[ "$recent_content" == 'yes' || "$recent_content" == 'event-driven' || "$recent_content" == 'event-driven-empty' ]]; then
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
REPORT_LINK_DIRECTORY="${report_markdown_file:h}" python3 "$report_generator" \
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
