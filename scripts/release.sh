#!/bin/bash

# 自动发布脚本
# 用法: ./scripts/release.sh <plugin> <version>
# 示例: ./scripts/release.sh ai-models 0.2.1

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 参数检查
if [ $# -ne 2 ]; then
    echo -e "${RED}错误: 参数不足${NC}"
    echo "用法: $0 <plugin> <version>"
    echo "示例: $0 ai-models 0.2.1"
    echo ""
    echo "可用的插件:"
    echo "  - ai-models      (qiniu-ai-models)"
    echo "  - storage-tools  (qiniu-storage-tools)"
    exit 1
fi

PLUGIN=$1
VERSION=$2

# 验证插件名
if [[ ! "$PLUGIN" =~ ^(ai-models|storage-tools)$ ]]; then
    echo -e "${RED}错误: 无效的插件名 '$PLUGIN'${NC}"
    echo "有效的插件名: ai-models, storage-tools"
    exit 1
fi

# 验证版本格式
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}错误: 无效的版本格式 '$VERSION'${NC}"
    echo "版本格式应为: x.y.z (例如: 0.2.1)"
    exit 1
fi

# 设置插件目录和名称
if [ "$PLUGIN" = "ai-models" ]; then
    PLUGIN_DIR="qiniu-ai-models"
    PLUGIN_NAME="qiniu-ai-models"
    PLUGIN_LABEL="七牛云 AI 模型"
else
    PLUGIN_DIR="qiniu-storage-tools"
    PLUGIN_NAME="qiniu-storage-tools"
    PLUGIN_LABEL="七牛云存储工具"
fi

MANIFEST_FILE="$PLUGIN_DIR/manifest.yaml"

# 检查插件目录是否存在
if [ ! -d "$PLUGIN_DIR" ]; then
    echo -e "${RED}错误: 插件目录不存在: $PLUGIN_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}准备发布 $PLUGIN_LABEL v$VERSION${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "2.x" ]; then
    echo -e "${YELLOW}警告: 当前分支是 '$CURRENT_BRANCH'，不是 'main' 或 '2.x'${NC}"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}已取消${NC}"
        exit 1
    fi
fi

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}警告: 存在未提交的更改${NC}"
    git status -s
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}已取消${NC}"
        exit 1
    fi
fi

# 检查 yq 是否安装
if ! command -v yq &> /dev/null; then
    echo -e "${RED}错误: 未找到 yq 命令${NC}"
    echo "请先安装 yq: brew install yq"
    exit 1
fi

# 获取当前版本
CURRENT_VERSION=$(yq eval '.version' "$MANIFEST_FILE")
echo -e "当前版本: ${YELLOW}$CURRENT_VERSION${NC}"
echo -e "新版本: ${GREEN}$VERSION${NC}"
echo ""

# 确认发布
read -p "确认发布? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}已取消${NC}"
    exit 1
fi

# 更新 manifest.yaml 版本
echo -e "${GREEN}[1/5]${NC} 更新 manifest.yaml 版本..."
yq eval ".version = \"$VERSION\"" -i "$MANIFEST_FILE"
echo -e "  ✓ 已更新 version: $VERSION"

# 清理缓存文件
echo -e "${GREEN}[2/5]${NC} 清理缓存文件..."
find "$PLUGIN_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PLUGIN_DIR" -name "*.pyc" -delete 2>/dev/null || true

# 提交更改
echo -e "${GREEN}[3/5]${NC} 提交更改..."
git add "$MANIFEST_FILE"
git commit -m "chore($PLUGIN): release version $VERSION"

# 创建标签
echo -e "${GREEN}[4/5]${NC} 创建 Git 标签..."
TAG_NAME="$PLUGIN_NAME-v$VERSION"
git tag -a "$TAG_NAME" -m "Release $PLUGIN_LABEL $VERSION"

# 推送到远程
echo -e "${GREEN}[5/5]${NC} 推送到远程仓库..."
git push origin "$CURRENT_BRANCH"
git push origin "$TAG_NAME"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}标签推送成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "插件: ${YELLOW}$PLUGIN_LABEL${NC}"
echo -e "版本: ${YELLOW}v$VERSION${NC}"
echo -e "标签: ${YELLOW}$TAG_NAME${NC}"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo -e "1. 在 GitHub 上创建 Release 以触发自动构建和发布"
echo -e "   ${YELLOW}https://github.com/qiniu/dify-plugin/releases/new?tag=$TAG_NAME${NC}"
echo ""
echo -e "2. Release 创建后，GitHub Actions 将自动:"
echo -e "   - 构建插件包 (${PLUGIN_NAME}-${VERSION}.difypkg)"
echo -e "   - 上传到 Release 资产"
echo ""
echo -e "3. 查看 Actions 进度:"
echo -e "   ${YELLOW}https://github.com/qiniu/dify-plugin/actions${NC}"
echo ""
