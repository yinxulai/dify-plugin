# 七牛云 Dify 插件

七牛云官方的 Dify 插件仓库，包含两个独立的插件：AI 模型插件和存储工具插件。

## 📦 插件列表

### 1. qiniu-ai-models - AI 模型插件

提供多种先进的大语言模型支持，包括 DeepSeek、Claude、GLM、Kimi、Qwen、Grok 等系列模型。

**主要功能：**
- 支持 15+ 先进 AI 模型
- 智能体思考、工具调用
- 流式响应和多工具调用
- 最高 256k 上下文支持

**安装地址：**
```
https://github.com/qiniu/dify-plugin.git#qiniu-ai-models
```

[查看详细文档 →](./qiniu-ai-models/readme/README.md)

---

### 2. qiniu-storage-tools - 存储工具插件

提供完整的七牛云对象存储管理功能。

**主要功能：**
- 列出存储空间
- 文件上传
- 文件列表查询（支持前缀过滤）
- 私有文件访问（签名链接）

**安装地址：**
```
https://github.com/qiniu/dify-plugin.git#qiniu-storage-tools
```

[查看详细文档 →](./qiniu-storage-tools/readme/README.md)

---

## 🚀 快速开始

### 安装插件

在 Dify 工作空间中：

1. 进入「插件」管理页面
2. 点击「安装插件」
3. 选择「从 GitHub 安装」
4. 输入对应插件的安装地址（见上方）

### 配置插件

#### AI 模型插件配置

- **API Key**：[获取七牛云 API Key](https://developer.qiniu.com/aitokenapi/12884/how-to-get-api-key)
- **API Endpoint**：默认 `https://openai.qiniu.com/v1`（可选）

#### 存储工具插件配置

- **Access Key**：[从控制台获取](https://portal.qiniu.com/user/key)
- **Secret Key**：[从控制台获取](https://portal.qiniu.com/user/key)

---

## ️ 开发说明

### 项目结构
```
dify-plugin/
├── qiniu-ai-models/          # AI 模型插件
│   ├── manifest.yaml
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── models/llm/
│   └── provider/
│
├── qiniu-storage-tools/      # 存储工具插件
│   ├── manifest.yaml
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── tools/
│   └── provider/
│
├── LICENSE
└── README.md
```

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/qiniu/dify-plugin.git
cd dify-plugin

# 安装 AI 模型插件依赖
cd qiniu-ai-models
pip install -r requirements.txt
cd ..

# 安装存储工具插件依赖
cd qiniu-storage-tools
pip install -r requirements.txt
```

#### 调试插件

1. 在 Dify 中获取远程调试地址和 Key
   - 参考：[Dify 插件调试文档](https://docs.dify.ai/plugins/quick-start/develop-plugins/debug-plugin)

2. 在对应插件目录创建 `.env` 文件：

   ```bash
   INSTALL_METHOD=remote
   REMOTE_INSTALL_PORT=5003
   REMOTE_INSTALL_URL=debug.dify.ai
   REMOTE_INSTALL_KEY=your-remote-key-here
   ```

3. 启动插件：

   ```bash
   python -m main
   ```

---

## 🚢 发布与部署

### 自动发布到官方插件仓库

本仓库已配置 GitHub Actions 自动发布工作流，当你推送代码到 `main` 或 `0.2.x` 分支时，会自动：

1. 打包插件为 `.difypkg` 文件
2. 推送到你 fork 的 `dify-plugins` 仓库
3. 自动创建 PR 到官方 `langgenius/dify-plugins` 仓库

**使用发布脚本（推荐）：**

```bash
# 交互式发布
./scripts/release.sh

# 指定插件和版本
./scripts/release.sh ai-models 0.0.2
./scripts/release.sh storage-tools 0.0.2
```

**配置要求：**
- 已 fork `langgenius/dify-plugins` 仓库
- 在本仓库设置 `PLUGIN_ACTION` Secret（GitHub Personal Access Token）
- 确保 `manifest.yaml` 中的 `author` 和 `version` 字段正确

详细配置指南请查看：[插件自动发布配置文档](./docs/AUTO_PUBLISH.md)

---

## 📋 版本历史

### v0.2.0 (2025-12-04)
- 🔄 重大更新：拆分为两个独立插件
- ✅ 符合 Dify 官方插件规范
- 📦 独立的 AI 模型插件和存储工具插件
- 🤖 新增自动发布 PR 到官方仓库功能

### v0.1.3 (之前版本)
- 包含 AI 模型和存储工具的完整版本

---

## 🤝 贡献指南

我们欢迎社区贡献！

### 🐛 报告 Bug

1. 检查 [Issues](https://github.com/qiniu/dify-plugin/issues) 是否已有相关问题
2. 提供详细信息：问题描述、复现步骤、环境信息、错误日志

### 💡 功能建议

在 [Issues](https://github.com/qiniu/dify-plugin/issues) 中创建功能建议，详细描述使用场景

### 🛠️ 代码贡献

1. Fork 此仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改（遵循下方 Commit 规范）
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

#### Commit 消息规范

使用语义化的 commit 消息格式：

```
<type>: <description>

[optional body]
```

**Type 类型：**
- `feat`: 新增功能
- `fix`: 修复问题
- `docs`: 文档更新
- `refactor`: 代码重构（不影响功能）
- `chore`: 构建/工具链更新
- `test`: 测试相关
- `style`: 代码格式调整

**示例：**
```bash
feat: add interactive mode to release script
fix: remove tool-related logic from AI models plugin
docs: update README with repository info
refactor: split into two independent plugins
chore(ai-models): release version 0.2.0
```

---

## 🤝 支持与反馈

- **问题反馈**：[GitHub Issues](https://github.com/qiniu/dify-plugin/issues)
- **功能建议**：欢迎提交 Issue 或 Pull Request
- **官方文档**：[七牛云开发者中心](https://developer.qiniu.com/)
- **官方网站**：[https://www.qiniu.com](https://www.qiniu.com)

---

## 📄 开源协议

本项目基于 [MIT License](./LICENSE) 开源。

---

**Made with ❤️ by Qiniu Cloud**
