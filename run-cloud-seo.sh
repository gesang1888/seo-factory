#!/usr/bin/env bash
# Thin wrapper for scripts/cloud_seo_optimize.py
set -euo pipefail
cd "$(dirname "$0")"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "Export CURSOR_API_KEY first: https://cursor.com/dashboard/integrations" >&2
  exit 1
fi

if [[ -z "${SEO_FACTORY_REPO_URL:-}" ]]; then
  echo "Tip: export SEO_FACTORY_REPO_URL='https://github.com/YOU/seo-factory'" >&2
fi

exec python3 scripts/cloud_seo_optimize.py "$@"
