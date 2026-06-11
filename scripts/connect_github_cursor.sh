#!/usr/bin/env bash
# Connect seo-factory to GitHub (SSH) + Cursor Cloud SDK env.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REPO_SSH="git@github.com:gesang1888/seo-factory.git"
REPO_HTTPS="https://github.com/gesang1888/seo-factory.git"
KEY_PATH="$HOME/.ssh/id_ed25519_github"
ENV_FILE="$ROOT/.env"

echo "==> seo-factory GitHub + Cursor SDK 连接助手"
echo

# --- SSH key for GitHub ---
if [[ ! -f "$KEY_PATH" ]]; then
  echo "生成 GitHub 专用 SSH 密钥..."
  mkdir -p "$HOME/.ssh"
  chmod 700 "$HOME/.ssh"
  ssh-keygen -t ed25519 -C "gesang1888@github-seo-factory" -f "$KEY_PATH" -N ""
  echo
  echo "请将下面公钥添加到 GitHub → Settings → SSH and GPG keys → New SSH key："
  echo "（已在浏览器打开 https://github.com/settings/keys ）"
  echo "----------------------------------------"
  cat "${KEY_PATH}.pub"
  echo "----------------------------------------"
  open "https://github.com/settings/keys" 2>/dev/null || true
  read -r -p "添加完公钥后按 Enter 继续..."
else
  echo "已存在 SSH 密钥: $KEY_PATH"
fi

# ssh config snippet
CFG="$HOME/.ssh/config"
if ! grep -q "Host github.com" "$CFG" 2>/dev/null; then
  mkdir -p "$HOME/.ssh"
  cat >> "$CFG" <<EOF

Host github.com
  HostName github.com
  User git
  IdentityFile $KEY_PATH
  IdentitiesOnly yes
EOF
  chmod 600 "$CFG"
  echo "已写入 ~/.ssh/config"
fi

# --- test github ssh ---
echo
echo "测试 GitHub SSH..."
if ssh -T -o StrictHostKeyChecking=accept-new git@github.com 2>&1 | grep -qi "successfully authenticated"; then
  echo "GitHub SSH 连接成功"
else
  echo "SSH 尚未通过。请确认公钥已添加到 GitHub，然后重新运行本脚本。"
  exit 1
fi

# --- ensure remote ---
git remote set-url origin "$REPO_SSH"

# --- create repo if missing ---
if ! git ls-remote origin &>/dev/null; then
  echo
  echo "远程仓库不存在或无权访问。请在浏览器创建空仓库："
  echo "  $REPO_HTTPS"
  open "https://github.com/new?name=seo-factory&owner=gesang1888" 2>/dev/null || true
  read -r -p "创建完仓库（不要勾选 README）后按 Enter 继续..."
fi

# --- push ---
echo
echo "推送代码到 GitHub..."
git push -u origin main

# --- Cursor env ---
echo
echo "==> Cursor SDK 环境变量"
if [[ ! -f "$ENV_FILE" ]]; then
  open "https://cursor.com/dashboard/integrations" 2>/dev/null || true
  echo "1. 在 Cursor Integrations 连接 GitHub 账号 gesang1888"
  echo "2. 创建 User API Key，复制 cursor_ 开头的 key"
  read -r -p "粘贴 CURSOR_API_KEY: " api_key
  cat > "$ENV_FILE" <<EOF
# seo-factory Cloud SEO — do not commit
CURSOR_API_KEY=$api_key
SEO_FACTORY_REPO_URL=$REPO_HTTPS
EOF
  chmod 600 "$ENV_FILE"
  echo "已写入 $ENV_FILE"
else
  echo "已存在 $ENV_FILE，跳过"
fi

echo
echo "加载环境并检查..."
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
python3 scripts/cloud_seo_check.py

echo
echo "连接完成。首次优化示例："
echo "  source $ENV_FILE && set -a && source $ENV_FILE && set +a"
echo "  ./run-cloud-seo.sh --task slugs --brand lovegobuy --slugs best-lovegobuy-spreadsheet --create-pr"
