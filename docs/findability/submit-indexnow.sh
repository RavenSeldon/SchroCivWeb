#!/usr/bin/env bash
# Submit the Schrödinger's Civilization URLs to IndexNow (one POST, shared by the
# protocol with every participating engine). Run on your Mac, from anywhere:
#
#   bash docs/findability/submit-indexnow.sh      (from the repo root)
#
# It refuses to submit unless (1) the key is live and exact, (2) every URL in
# urls-tale-first.txt answers 200, and (3) every URL is under the canonical path.
# Safe to re-run later (e.g. after a redeploy); IndexNow asks you not to spam it.
set -euo pipefail

KEY="bb04f9030ee793b9013b131113bf5e1c"
HOST="benamuwo.me"
KEY_URL="${KEY_URL:-https://${HOST}/${KEY}.txt}"
URL_PREFIX="${URL_PREFIX:-https://${HOST}/schrodingers_civ/}"
ENDPOINT="${INDEXNOW_ENDPOINT:-https://api.indexnow.org/indexnow}"
HERE="$(cd "$(dirname "$0")" && pwd)"
URLS_FILE="${URLS_FILE:-${HERE}/urls-tale-first.txt}"

echo "1/3  Key file: ${KEY_URL}"
body="$(curl -fsS --max-time 20 "$KEY_URL")" || { echo "ABORT: key file not reachable. Install docs/findability/nginx-indexnow-key.conf first."; exit 1; }
[ "$body" = "$KEY" ] || { echo "ABORT: key file content is not exactly the key."; exit 1; }

echo "2/3  Checking every URL answers 200"
n=0
while IFS= read -r u || [ -n "$u" ]; do
  case "$u" in ''|'#'*) continue ;; esac
  case "$u" in "$URL_PREFIX"*) ;; *) echo "ABORT: $u is outside $URL_PREFIX"; exit 1 ;; esac
  code="$(curl -s -o /dev/null --max-time 20 -w '%{http_code}' "$u")"
  [ "$code" = "200" ] || { echo "ABORT: $u answered $code"; exit 1; }
  n=$((n + 1))
done < "$URLS_FILE"
echo "     ${n} URLs OK"

# (python3 -c rather than a heredoc inside $(...): macOS's bash 3.2 misparses the latter)
payload="$(python3 -c 'import json, sys
urls = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]
print(json.dumps({"host": sys.argv[2], "key": sys.argv[3], "keyLocation": sys.argv[4], "urlList": urls}))' \
  "$URLS_FILE" "$HOST" "$KEY" "$KEY_URL")"

echo "3/3  POST ${ENDPOINT}"
resp="$(mktemp)"
code="$(curl -s -o "$resp" --max-time 30 -w '%{http_code}' -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json; charset=utf-8' --data "$payload")"
cat "$resp"; rm -f "$resp"
case "$code" in
  200) echo "IndexNow 200: accepted." ;;
  202) echo "IndexNow 202: received; key validation pending." ;;
  403) echo "IndexNow 403: key not valid (file missing or wrong)."; exit 1 ;;
  422) echo "IndexNow 422: URLs don't match host/key."; exit 1 ;;
  429) echo "IndexNow 429: too many requests; wait before retrying."; exit 1 ;;
  *)   echo "IndexNow answered ${code}."; exit 1 ;;
esac
