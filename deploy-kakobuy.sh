#!/usr/bin/env bash
# Build + deploy Kakobuy 5-domain cluster to Baota VPS.
# Usage:
#   export KAKOBUY_DEPLOY_PASS='your-ssh-password'
#   ./deploy-kakobuy.sh
#
# Files only (skip certs/nginx/baota):
#   KAKOBUY_SKIP_CERTS=1 KAKOBUY_SKIP_NGINX=1 KAKOBUY_SKIP_BAOTA=1 ./deploy-kakobuy.sh

set -euo pipefail
cd "$(dirname "$0")"

echo "==> build"
python3 build_kakobuy_site.py

echo "==> deploy"
python3 scripts/deploy_kakobuy.py
