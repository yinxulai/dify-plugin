# Qiniu AI Models Plugin

Official Qiniu Cloud AI inference plugin for Dify, providing access to multiple advanced large language models.

## 📦 Plugin Information

- **Plugin Name**: ai-models-provider
- **Author**: Qiniu Cloud
- **Version**: 0.2.0
- **License**: MIT License

## Features

### 🤖 Supported AI Models

This plugin connects to Qiniu Cloud AI inference platform, supporting multiple mainstream large language models, including but not limited to:

- **DeepSeek Series**: DeepSeek-R1, DeepSeek-V3, and other inference-optimized models
- **Claude Series**: Anthropic Claude 3.5/4.x series advanced models
- **GLM Series**: Zhipu GLM-4.x series Chinese-optimized models
- **Qwen Series**: Alibaba Qwen3 series models
- **Gemini Series**: Google Gemini 2.x/3.x series models
- **Kimi Series**: Moonshot Kimi-K2 and other long-context models
- **Other Models**: Grok, Doubao, MiniMax, and more

> 💡 **Note**: The model list is continuously updated. For the complete list, please check the Dify model provider configuration page or visit [Qiniu Cloud AI Platform](https://openai.qiniu.com/) for the latest supported models.

### ✨ Core Capabilities

All models support the following advanced features:

- ✅ Agent Thinking
- ✅ Tool Calling
- ✅ Multi-tool Calling
- ✅ Streaming Tool Calls
- ✅ Streaming Response

## Installation

### Install in Dify

1. Open Dify workspace
2. Go to "Plugins" management page
3. Select "Install Plugin"
4. Choose one of the following installation methods:

#### Method 1: Install from GitHub Repository (Recommended)

```
https://github.com/qiniu/dify-plugin
```

#### Method 2: Install from Official Marketplace

Search for "Qiniu AI Models" in the plugin marketplace

### Configure Plugin

1. After successful installation, find "Qiniu AI Models" in the plugin list
2. Click the "Configure" button
3. Fill in the following information:

   - **API Key**: Your Qiniu Cloud API key (required)
   - **API Endpoint URL**: Custom API endpoint (optional, default: https://openai.qiniu.com/v1)

4. Click "Save" to complete configuration

### Get API Key

1. Visit [Qiniu Cloud Developer Center](https://developer.qiniu.com/aitokenapi/12884/how-to-get-api-key)
2. Log in to your Qiniu Cloud account
3. Get your API Key from the API management page

## Usage Example

After configuration, you can use Qiniu Cloud AI models in Dify applications:

1. In the application orchestration page, select "Model Provider"
2. Find the "Qiniu Cloud" provider
3. Select the model you need (e.g., DeepSeek-V3, Claude 4.5 Sonnet, etc.)
4. Start using!

## Technical Specifications

- **Architecture Support**: AMD64, ARM64
- **Runtime Environment**: Python 3.12
- **Memory Requirements**: 256 MB
- **Dependencies**:
  - dify_plugin >= 0.3.0, < 0.5.0
  - requests >= 2.25.0

## Related Plugins

For Qiniu Cloud object storage functionality, please also install:

- **storage-tools**: Qiniu Cloud Storage Tools Plugin

## Support and Feedback

- **Issue Reporting**: [GitHub Issues](https://github.com/qiniu/dify-plugin/issues)
- **Documentation**: [Qiniu Cloud Developer Documentation](https://developer.qiniu.com/)
- **Official Website**: [https://www.qiniu.com](https://www.qiniu.com)

## License

This plugin is open-sourced under the MIT License. See [LICENSE](../../LICENSE) file for details.

---

Made with ❤️ by Qiniu Cloud
