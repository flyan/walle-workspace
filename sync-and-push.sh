#!/bin/bash
# sync-and-push.sh
# 自动同步所有 agent 工作目录到主仓库，然后提交和推送到 GitHub

WORKSPACE_ROOT="/c/Users/flyan/.openclaw/workspace"
AGENTS_WORKSPACES_DIR="$WORKSPACE_ROOT/agents-workspaces"
WRITER_EXTERNAL="/c/Users/flyan/.openclaw/workspace-writer"
CODER_EXTERNAL="/c/Users/flyan/.openclaw/workspace-coder"

COMMIT_MESSAGE="${1:-Auto-sync: Update agents workspaces}"

echo "🔄 开始同步 agents 工作目录..."

# 同步 writer
if [ -d "$WRITER_EXTERNAL" ]; then
    echo "  📁 同步 writer..."
    WRITER_TARGET="$AGENTS_WORKSPACES_DIR/writer"
    
    rm -rf "$WRITER_TARGET"
    mkdir -p "$WRITER_TARGET"
    
    cp -r "$WRITER_EXTERNAL"/* "$WRITER_TARGET/" 2>/dev/null || true
    
    echo "    ✓ writer 同步完成"
fi

# 同步 coder
if [ -d "$CODER_EXTERNAL" ]; then
    echo "  📁 同步 coder..."
    CODER_TARGET="$AGENTS_WORKSPACES_DIR/coder"
    
    rm -rf "$CODER_TARGET"
    mkdir -p "$CODER_TARGET"
    
    cp -r "$CODER_EXTERNAL"/* "$CODER_TARGET/" 2>/dev/null || true
    
    echo "    ✓ coder 同步完成"
fi

echo ""
echo "📊 检查 git 状态..."

cd "$WORKSPACE_ROOT"

# 检查是否有变更
if [ -z "$(git status --short)" ]; then
    echo "✓ 没有新的变更，无需提交"
    exit 0
fi

echo "发现以下变更:"
git status --short

echo ""
echo "📝 添加文件到 git..."

git add -A
echo "✓ 文件已添加"

echo ""
echo "💾 提交变更..."

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
FULL_MESSAGE="$COMMIT_MESSAGE ($TIMESTAMP)"
git commit -m "$FULL_MESSAGE"
echo "✓ 提交完成: $FULL_MESSAGE"

echo ""
echo "🚀 推送到 GitHub..."

git push origin main
echo "✓ 推送完成"

echo ""
echo "✅ 同步和推送完成！"

echo ""
echo "📌 最新 commit:"
git log --oneline -1
