#!/usr/bin/env bash
# archive-catalog · 一键安装脚本
# 用法: bash install.sh [目标目录，默认 ~/.claude/skills]
set -euo pipefail

REPO_URL="https://github.com/xinqing520/archive-catalog.git"
SKILL_NAME="archive-catalog"
DEST="${1:-$HOME/.claude/skills}"

echo "▶ 安装 $SKILL_NAME skill → $DEST"
mkdir -p "$DEST"

if [ -d "$DEST/$SKILL_NAME" ]; then
  echo "  目标已存在，执行更新…"
  git -C "$DEST/$SKILL_NAME" pull --ff-only
else
  echo "  克隆仓库…"
  git clone "$REPO_URL" "$DEST/$SKILL_NAME"
fi

echo ""
echo "✅ 安装完成: $DEST/$SKILL_NAME"
echo "  在 Claude Code 会话中运行 /skills 确认出现 archive-catalog。"
echo "  触发词:「处理档案目录」「合并总目录」「档号规范化」「OCR修正」"
