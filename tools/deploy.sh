#!/bin/zsh
# Build the public site into dist/ and deploy it to Cloudflare (Workers static assets, see wrangler.jsonc).
#   tools/deploy.sh                 -> deploy
#   DRY_RUN=1 tools/deploy.sh       -> build dist/ only (used by the local preview)
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
rsync -a --exclude dist --exclude tools --exclude .git --exclude .claude --exclude CNAME --exclude wrangler.jsonc --exclude .gitignore --exclude '.DS_Store' ./ dist/
[[ ${DRY_RUN:-0} == 1 ]] && { echo "built dist/"; exit 0; }
wrangler deploy
