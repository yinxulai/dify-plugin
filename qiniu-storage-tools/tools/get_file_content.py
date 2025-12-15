import json
import logging
import requests
from collections.abc import Generator
from typing import Any

from qiniu import Auth
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

logger = logging.getLogger(__name__)


class QiniuGetContentTool(Tool):
    """
    七牛云获取文件内容工具
    
    通过文件 key 和域名获取签名 URL 并读取文件内容
    """

    def _get_auth(self) -> Auth:
        """获取七牛云认证对象"""
        access_key = self.runtime.credentials.get("qiniu_access_key")
        secret_key = self.runtime.credentials.get("qiniu_secret_key")
        
        if not access_key or not secret_key:
            raise ToolProviderCredentialValidationError("七牛云 Access Key 和 Secret Key 不能为空")
        
        return Auth(access_key, secret_key)

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        获取七牛云文件内容
        
        Args:
            tool_parameters: 工具参数
                - file_key: 文件的 key（路径）
                - domain: 七牛云绑定的域名
                - expire_time: 链接有效期（秒），默认 3600 秒
                
        Returns:
            Generator[ToolInvokeMessage, None, None]: 工具调用消息生成器
        """
        file_key = tool_parameters.get("file_key", "").strip()
        domain = tool_parameters.get("domain", "").strip()
        expire_time = tool_parameters.get("expire_time", 3600)
        
        # 参数验证
        if not file_key:
            yield self.create_text_message("文件 key 不能为空")
            return
            
        if not domain:
            yield self.create_text_message("域名不能为空")
            return
            
        # 确保域名格式正确
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
            
        try:
            # 获取认证对象
            auth = self._get_auth()
            
            # 生成私有下载链接
            base_url = f"{domain}/{file_key}"
            private_url = auth.private_download_url(base_url, expires=expire_time)
            
            yield self.create_text_message("正在获取文件内容...")
            
            # 请求文件内容
            response = requests.get(private_url, timeout=30)
            response.raise_for_status()
            
            # 获取文件内容
            content = response.text
            content_type = response.headers.get('content-type', 'text/plain')
            file_size = len(response.content)
            
            # 检查文件大小（限制在 10MB 以内）
            max_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_size:
                yield self.create_text_message(
                    f"文件过大（{file_size/1024/1024:.2f}MB），超过 10MB 限制"
                )
                return
            
            # 返回结果
            result = {
                "success": True,
                "file_key": file_key,
                "domain": domain,
                "content_type": content_type,
                "file_size": file_size,
                "content": content,
                "signed_url": private_url
            }
            
            # 创建简化的文本结果
            markdown_content = f"文件内容获取成功：{file_key}（{file_size/1024:.2f} KB）"
            
            yield self.create_text_message(markdown_content)
            
            # 创建文件 blob 消息，供大模型直接使用
            blob_meta = {
                "file_key": file_key,
                "file_name": file_key.split('/')[-1],  # 从 key 中提取文件名
                "file_size": file_size,
                "content_type": content_type,
                "domain": domain
            }
            yield self.create_blob_message(response.content, meta=blob_meta)
            
            # 返回 JSON 格式的详细结果
            yield self.create_json_message(result)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"文件不存在: {file_key}"
                status_desc = "文件未找到"
            elif e.response.status_code == 403:
                error_msg = "访问被拒绝，请检查文件权限或域名配置"
                status_desc = "访问权限不足"
            else:
                error_msg = f"HTTP 错误: {e.response.status_code}"
                status_desc = f"HTTP {e.response.status_code} 错误"
            
            # 创建 HTTP 错误的简化消息
            markdown_content = f"获取失败：{error_msg}"
            
            logger.error(error_msg)
            yield self.create_text_message(markdown_content)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求失败: {str(e)}"
            
            # 创建网络错误的简化消息
            markdown_content = f"网络错误：{error_msg}"
            
            logger.error(error_msg)
            yield self.create_text_message(markdown_content)
            
        except Exception as e:
            error_msg = f"获取文件内容失败: {str(e)}"
            
            # 创建通用错误的简化消息
            markdown_content = f"系统错误：{error_msg}"
            
            logger.error(error_msg, exc_info=True)
            yield self.create_text_message(markdown_content)
