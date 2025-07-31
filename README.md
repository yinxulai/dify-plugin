# 七牛云 AI 模型插件

七牛云官方的 Dify 插件，为 Dify 平台提供七牛云 AI 模型服务支持。

![七牛云 AI](assets/qiniu_ai.png)

## 功能特性

- ✅ **AI 推理模型供应商**：支持多种先进的 AI 大语言模型
- 🔄 **对象存储**（开发中）

## 安装使用

### 方式一：插件市场安装（推荐）

1. 访问 [Dify 插件市场](https://marketplace.dify.ai)
2. 搜索"七牛云"或"Qiniu"
3. 点击安装并按照提示配置

### 方式二：手动安装

1. 下载本插件源码
2. 在 Dify 中选择"本地插件"安装方式
3. 上传插件包并配置

## 配置说明

### 必需配置

- **API Key**：在 [七牛云 AI 推理控制台](https://portal.qiniu.com/ai-inference/api-key) 获取

### 可选配置

- **Custom API endpoint URL**：自定义 API 接口地址
  - 默认：`https://openai.qiniu.com/v1`
  - 格式示例：`https://api.qiniu.com/v1` 或 `https://api.qiniu.com`

## 开发指南

### 环境要求

- Python 3.12+
- dify_plugin >= 0.3.0, < 0.4.0

### 开发步骤

#### 1. 初始化开发环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置调试环境

1. 在 Dify 中获取远程调试地址和 Key
   - 参考：[Dify 插件调试文档](https://docs.dify.ai/zh-hans/plugins/quick-start/debug-plugin)

2. 复制环境配置文件：

   ```bash
   cp .env.example .env
   ```

3. 编辑 `.env` 文件，填入调试配置：

   ```bash
   INSTALL_METHOD=remote
   REMOTE_INSTALL_PORT=5003
   REMOTE_INSTALL_KEY=your-debug-key-here
   REMOTE_INSTALL_HOST=debug-plugin.dify.dev
   ```

#### 3. 启动插件

```bash
python -m main
```

## 许可证

本项目采用 MIT 开源许可证，具体详情请查看 LICENSE 文件。
