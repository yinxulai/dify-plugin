import json
import logging
from collections.abc import Generator
from typing import Any

from qiniu import Auth, put_data, BucketManager
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

logger = logging.getLogger(__name__)


class QiniuUploadTool(Tool):
    """
    七牛云上传工具
    
    支持上传内容到指定的七牛云存储空间，并返回访问链接
    """

    def _get_auth(self) -> Auth:
        """获取七牛云认证对象"""
        access_key = self.runtime.credentials.get("qiniu_access_key")
        secret_key = self.runtime.credentials.get("qiniu_secret_key")
        
        if not access_key or not secret_key:
            raise ToolProviderCredentialValidationError("七牛云 Access Key 和 Secret Key 不能为空")
        
        return Auth(access_key, secret_key)

    def _validate_bucket_access(self, bucket_name: str) -> bool:
        """验证存储空间访问权限"""
        try:
            auth = self._get_auth()
            bucket_manager = BucketManager(auth)
            
            # 尝试获取空间列表来验证认证信息
            ret, eof, info = bucket_manager.list(bucket_name, limit=1)
            
            if info.status_code == 200:
                return True
            elif info.status_code == 401:
                raise ToolProviderCredentialValidationError("七牛云认证失败，请检查 Access Key 和 Secret Key")
            elif info.status_code == 631:
                raise ToolProviderCredentialValidationError(f"存储空间 '{bucket_name}' 不存在")
            else:
                raise ToolProviderCredentialValidationError(f"验证存储空间失败: {info.error}")
                
        except Exception as e:
            if isinstance(e, ToolProviderCredentialValidationError):
                raise
            raise ToolProviderCredentialValidationError(f"验证存储空间时发生错误: {str(e)}")

    def _apply_prefix(self, filename: str, prefix: str = None) -> str:
        """应用前缀到文件名"""
        if not prefix:
            return filename
        
        # 确保前缀格式正确
        prefix = prefix.strip()
        if prefix and not prefix.endswith('/'):
            prefix += '/'
        
        return f"{prefix}{filename}"

    def _upload_to_qiniu(self, content: str, filename: str, bucket: str, overwrite: bool = False) -> dict:
        """上传内容到七牛云"""
        try:
            auth = self._get_auth()
            
            # 根据覆盖设置生成上传凭证
            if overwrite:
                # 允许覆盖同名文件
                token = auth.upload_token(bucket, filename)
            else:
                # 不允许覆盖，如果文件存在会返回错误
                policy = {
                    'scope': f'{bucket}:{filename}',
                    'insertOnly': 1  # 仅当文件不存在时才允许上传
                }
                token = auth.upload_token(bucket, filename, policy=policy)
            
            # 上传内容
            ret, info = put_data(token, filename, content.encode('utf-8'))
            
            if info.status_code == 200:
                return {
                    "success": True,
                    "key": ret.get("key", filename),
                    "hash": ret.get("hash", ""),
                    "bucket": bucket
                }
            else:
                error_msg = f"上传失败: HTTP {info.status_code}"
                if hasattr(info, 'error') and info.error:
                    error_msg += f" - {info.error}"
                    # 特殊处理文件已存在的情况
                    if info.status_code == 614:
                        error_msg = "文件已存在且未设置覆盖选项"
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"上传过程中发生错误: {str(e)}"
            }

    def _generate_access_url(self, key: str, bucket: str, domain: str = None) -> str:
        """生成访问链接"""
        if domain:
            # 如果提供了自定义域名，生成完整的访问链接
            domain = domain.rstrip('/')
            if not domain.startswith(('http://', 'https://')):
                domain = f"https://{domain}"
            return f"{domain}/{key}"
        else:
            # 如果没有提供域名，返回文件路径
            return key

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        执行七牛云上传操作
        
        Args:
            tool_parameters: 工具参数，包含 content, filename, bucket, domain(可选), overwrite(可选), prefix(可选)
            
        Yields:
            ToolInvokeMessage: 工具执行结果消息
        """
        try:
            # 获取参数
            content = tool_parameters.get("content", "")
            filename = tool_parameters.get("filename", "")
            prefix = tool_parameters.get("prefix", "")
            bucket = tool_parameters.get("bucket", "")
            domain = tool_parameters.get("domain", "")
            overwrite = tool_parameters.get("overwrite", False)
            
            # 验证必需参数
            if not content:
                yield self.create_text_message("上传内容不能为空")
                return
                
            if not filename:
                yield self.create_text_message("文件名不能为空")
                return
                
            if not bucket:
                yield self.create_text_message("存储空间名称不能为空")
                return

            # 应用前缀到文件名
            final_filename = self._apply_prefix(filename, prefix)

            # 验证存储空间访问权限
            self._validate_bucket_access(bucket)
            
            # 执行上传
            upload_result = self._upload_to_qiniu(content, final_filename, bucket, overwrite)
            
            if upload_result["success"]:
                # 生成访问链接
                access_url = self._generate_access_url(
                    upload_result["key"], 
                    bucket, 
                    domain if domain else None
                )
                
                # 创建简化的成功消息
                markdown_content = f"文件上传成功：{final_filename}"
                
                yield self.create_text_message(markdown_content)
                
                # 简化输出，只返回三个核心信息
                result = {
                    "file_key": upload_result["key"],  # 文件在存储桶中的路径
                    "file_url": access_url if domain else None,  # 如果配置了域名则返回完整URL，否则为None
                    "error": None  # 成功时错误为None
                }
                
                yield self.create_json_message(result)
            else:
                # 创建简化的失败消息
                markdown_content = f"文件上传失败：{upload_result['error']}"
                
                yield self.create_text_message(markdown_content)
                
                # 上传失败，返回错误信息
                result = {
                    "file_key": None,
                    "file_url": None,
                    "error": upload_result['error']
                }
                yield self.create_json_message(result)
                
        except ToolProviderCredentialValidationError as e:
            # 创建认证错误的简化消息
            markdown_content = f"认证错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 认证错误
            result = {
                "file_key": None,
                "file_url": None,
                "error": f"认证错误：{str(e)}"
            }
            yield self.create_json_message(result)
        except Exception as e:
            logger.exception("七牛云上传工具执行失败")
            
            # 创建通用错误的简化消息
            markdown_content = f"系统错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 其他错误
            result = {
                "file_key": None,
                "file_url": None,
                "error": f"执行失败：{str(e)}"
            }
            yield self.create_json_message(result)
