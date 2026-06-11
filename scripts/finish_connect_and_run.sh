#!/usr/bin/env bash
# After adding SSH key to GitHub and CURSOR_API_KEY to .env, run steps 1–4.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

set -a
# shellcheck disable=SC1091
[[ -f .env ]] && source .env
set +a

echo "==> [1/4] git push"
if ! ssh -T -o ConnectTimeout=10 git@github.com 2>&1 | grep -qi "successfully authenticated"; then
  echo "GitHub SSH 未通过。请在 https://github.com/settings/ssh/new 添加公钥："
  cat "$HOME/.ssh/id_ed25519_github.pub"
  exit 1
fi
git push -u origin main
echo "Push OK"

echo "==> [2/4] .env"
if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  read -r -p "粘贴 CURSOR_API_KEY (cursor_...): " CURSOR_API_KEY
  if grep -q '^CURSOR_API_KEY=' .env 2>/dev/null; then
    sed -i '' "s|^CURSOR_API_KEY=.*|CURSOR_API_KEY=$CURSOR_API_KEY|" .env
  else
    echo "CURSOR_API_KEY=$CURSOR_API_KEY" >> .env
  fi
  export CURSOR_API_KEY
fi
export SEO_FACTORY_REPO_URL="${SEO_FACTORY_REPO_URL:-https://github.com/gesang1888/seo-factory}"

echo "==> [3/4] preflight"
python3 scripts/cloud_seo_check.py

echo "==> [4/4] first Cloud SEO run"
./run-cloud-seo.sh --task slugs --brand lovegobuy \
  --slugs best-lovegobuy-spreadsheet \
  --domain lovegobuyspreadsheet.nl \
  --create-pr
