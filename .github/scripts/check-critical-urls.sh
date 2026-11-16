#!/usr/bin/env bash
# Checks the critical live URLs from .github/critical-urls.txt:
# each must answer HTTP 200 after redirects and, if given, contain a text marker.
# Used by .github/workflows/links.yml (job "critical"); also runs locally:
#   .github/scripts/check-critical-urls.sh [.github/critical-urls.txt]
set -uo pipefail

list="${1:-.github/critical-urls.txt}"
summary="${GITHUB_STEP_SUMMARY:-/dev/null}"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
failed=0

{
  echo "## Critical URLs"
  echo
  echo "| Result | Status | URL | Marker |"
  echo "|---|---|---|---|"
} >> "$summary"

while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%$'\r'}"
  [[ -z "${line// }" || "$line" =~ ^[[:space:]]*# ]] && continue
  url="${line%% | *}"
  url="${url// /}"
  marker=""
  [[ "$line" == *" | "* ]] && marker="${line#* | }"

  status="$(curl -sS -L --max-redirs 5 --retry 3 --retry-delay 5 --retry-all-errors \
    --connect-timeout 15 --max-time 45 \
    -A "Mozilla/5.0 (compatible; mitjamartini-linkcheck; +https://github.com/mitja/mitja.github.io)" \
    -o "$tmp" -w '%{http_code}' "$url" 2>&1 | tail -n1)"

  result="OK"
  marker_result="-"
  if [[ "$status" != "200" ]]; then
    result="FAIL"
  elif [[ -n "$marker" ]]; then
    if grep -qF -- "$marker" "$tmp"; then
      marker_result="found: $marker"
    else
      marker_result="MISSING: $marker"
      result="FAIL"
    fi
  fi

  if [[ "$result" == "FAIL" ]]; then
    failed=1
    echo "::error title=Critical URL broken::$url -> HTTP $status, marker: $marker_result"
  fi
  echo "$result  $status  $url  $marker_result"
  echo "| $result | $status | $url | $marker_result |" >> "$summary"
done < "$list"

exit "$failed"
