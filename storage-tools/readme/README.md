# Qiniu Storage Tools Plugin

Official Qiniu Cloud object storage tools plugin for Dify, providing comprehensive cloud storage management capabilities.

## 📦 Plugin Information

- **Plugin Name**: qiniu-storage-tools
- **Author**: Qiniu Cloud
- **Version**: 0.2.0
- **License**: MIT License

## Features

### 📁 Object Storage Tools

Provides complete Qiniu Cloud storage management functionality:

#### 1. List Buckets

View all storage buckets (Bucket) under your account.

- **Functionality**: Get all available storage buckets
- **Returns**: List of bucket names
- **Use case**: Understand your storage resource distribution

#### 2. File Upload

Upload files to a specified storage bucket.

- **Supported Features**:
  - Specify target storage bucket
  - Custom file prefix/path
  - Set custom domain
  - Return file access link
- **Use case**: Store application-generated files, images, and other resources

#### 3. List Files

View the file list in a storage bucket.

- **Supported Features**:
  - Filter files by prefix
  - Paginated query
  - Limit number of results
- **Use case**: Browse and manage files in storage buckets

#### 4. Get File Content

Get access links or content for private files.

- **Supported Features**:
  - Generate signed access links
  - Support private bucket file access
  - Set link expiration time
- **Use case**: Securely access and share private files

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

Search for "Qiniu Storage Tools" in the plugin marketplace

### Configure Plugin

1. After successful installation, find "Qiniu Storage Tools" in the plugin list
2. Click the "Configure" button
3. Fill in the following information:

   - **Access Key**: Your Qiniu Cloud Access Key (required)
   - **Secret Key**: Your Qiniu Cloud Secret Key (required)

4. Click "Save" to complete configuration

### Get Credentials

1. Visit [Qiniu Cloud Console](https://portal.qiniu.com/user/key)
2. Log in to your Qiniu Cloud account
3. View or create your Access Key and Secret Key in the "Key Management" page

## Usage Example

After configuration, you can use Qiniu Cloud storage tools in Dify applications:

### Use in Workflow

1. In the workflow orchestration page, add a "Tool" node
2. Select the "Qiniu Cloud Storage" toolset
3. Select the tool you need (e.g., file upload, list files, etc.)
4. Configure tool parameters
5. Connect to other nodes and run

### Use in Agent

1. Create an Agent application
2. Enable "Qiniu Cloud Storage" in tool configuration
3. The Agent will automatically call storage tools as needed

## Use Cases

- **File Management**: Automate management of cloud files and resources
- **Content Generation**: Automatically upload AI-generated content (e.g., images, documents) to cloud storage
- **Data Processing**: Read data from cloud storage for analysis and processing
- **Resource Sharing**: Generate secure temporary access links for file sharing

## Technical Specifications

- **Architecture Support**: AMD64, ARM64
- **Runtime Environment**: Python 3.12
- **Memory Requirements**: 256 MB
- **Dependencies**:
  - dify_plugin >= 0.3.0, < 0.5.0
  - qiniu >= 7.12.0

## Related Plugins

For Qiniu Cloud AI inference models, please also install:

- **ai-models-provider**: Qiniu Cloud AI Models Plugin

## Support and Feedback

- **Issue Reporting**: [GitHub Issues](https://github.com/qiniu/dify-plugin/issues)
- **Documentation**: [Qiniu Cloud Developer Documentation](https://developer.qiniu.com/)
- **Official Website**: [https://www.qiniu.com](https://www.qiniu.com)

## License

This plugin is open-sourced under the MIT License. See [LICENSE](../../LICENSE) file for details.

---

Made with ❤️ by Qiniu Cloud
