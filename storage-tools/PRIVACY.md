# Privacy Policy

## Data Collection

This plugin does **not** collect, store, or transmit any personal data on its own.

## How This Plugin Works

This plugin uses the [Qiniu Cloud Object Storage (Kodo) API](https://developer.qiniu.com/kodo) to perform file and bucket operations. The data flow is:

1. File upload/download requests are sent directly from Dify to Qiniu Cloud's storage service.
2. File metadata and content are transmitted to or retrieved from Qiniu Cloud's servers.
3. This plugin does not store, log, or share any of this data independently.

## Third-Party Services

All storage operations are performed by **Qiniu Cloud Kodo**. By using this plugin, your data is subject to:

- [Qiniu Cloud Privacy Policy](https://www.qiniu.com/privacy)
- [Qiniu Cloud Terms of Service](https://www.qiniu.com/agreements)

## Credentials

Your Qiniu Cloud API credentials (Access Key / Secret Key) are stored securely within your Dify instance and are only used to authenticate requests to Qiniu Cloud's storage API.

## Contact

For privacy-related questions, please contact: support@qiniu.com
