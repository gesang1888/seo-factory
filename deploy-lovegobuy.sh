#!/usr/bin/env bash
# Build + deploy Lovegobuy 8-domain cluster to Baota VPS.
# Usage:
#   export LOVEGOBUY_DEPLOY_PASS='your-ssh-password'
#   ./deploy-lovegobuy.sh
#
# Files only:
#   LOVEGOBUY_SKIP_CERTS=1 LOVEGOBUY_SKIP_NGINX=1 LOVEGOBUY_SKIP_BAOTA=1 ./deploy-lovegobuy.sh

set -euo pipefail
cd "$(dirname "$0")"

echo "==> build"
python3 build_lovegobuy_site.py

echo "==> deploy"
python3 scripts/deploy_lovegobuy.py
