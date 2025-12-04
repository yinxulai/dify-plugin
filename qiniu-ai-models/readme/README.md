# Qiniu AI Models Plugin

Official Qiniu Cloud AI inference plugin for Dify, providing access to multiple advanced large language models.

## 📦 Plugin Information

- **Plugin Name**: qiniu-ai-models
- **Author**: Qiniu Cloud
- **Version**: 0.2.0
- **License**: MIT License

## Features

### 🤖 Supported AI Models

This plugin supports the following advanced large language models:

- **OpenAI OSS Series**: GPT-OSS-120b, GPT-OSS-20b
- **DeepSeek Series**: DeepSeek-R1, DeepSeek-V3, DeepSeek-V3.1 (128k context)
- **Claude Series**: Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude 4.0 Sonnet, Claude 4.5 Sonnet, Claude 4.0 Opus, Claude 4.1 Opus (200k context)
- **GLM Series**: GLM-4.5, GLM-4.5-Air
- **Kimi Series**: Kimi-K2
- **Qwen Series**: Qwen-Turbo, Qwen3-32B, Qwen3-235B-A22B (128k context), Qwen3-Max-Preview (256k context)
- **Grok Series**: Grok Code Fast 1 (256k context, code-optimized)

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
https://github.com/qiniu/dify-plugin.git#qiniu-ai-models
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

- **qiniu-storage-tools**: Qiniu Cloud Storage Tools Plugin

## Support and Feedback

- **Issue Reporting**: [GitHub Issues](https://github.com/qiniu/dify-plugin/issues)
- **Documentation**: [Qiniu Cloud Developer Documentation](https://developer.qiniu.com/)
- **Official Website**: [https://www.qiniu.com](https://www.qiniu.com)

## License

This plugin is open-sourced under the MIT License. See [LICENSE](../../LICENSE) file for details.

---

Made with ❤️ by Qiniu Cloud
