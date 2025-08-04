import json
import logging
from collections.abc import Generator
from typing import Any

from qiniu import Auth, BucketManager
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

logger = logging.getLogger(__name__)


class QiniuListBucketsTool(Tool):
    """
    七牛云存储空间列表工具
    
    获取当前账户下的所有存储空间列表
    """

    def _get_auth(self) -> Auth:
        """获取七牛云认证对象"""
        access_key = self.runtime.credentials.get("qiniu_access_key")
        secret_key = self.runtime.credentials.get("qiniu_secret_key")
        
        if not access_key or not secret_key:
            raise ToolProviderCredentialValidationError("七牛云 Access Key 和 Secret Key 不能为空")
        
        return Auth(access_key, secret_key)

    def _list_buckets(self) -> dict:
        """获取存储空间列表"""
        try:
            auth = self._get_auth()
            bucket_manager = BucketManager(auth)
            
            # 获取存储空间列表
            ret, info = bucket_manager.buckets()
            
            if info.status_code == 200:
                return {
                    "success": True,
                    "buckets": ret if ret else [],
                    "count": len(ret) if ret else 0
                }
            elif info.status_code == 401:
                raise ToolProviderCredentialValidationError("七牛云认证失败，请检查 Access Key 和 Secret Key")
            else:
                return {
                    "success": False,
                    "error": f"获取存储空间列表失败: HTTP {info.status_code} - {info.error if hasattr(info, 'error') else ''}"
                }
                
        except Exception as e:
            if isinstance(e, ToolProviderCredentialValidationError):
                raise
            return {
                "success": False,
                "error": f"获取存储空间列表时发生错误: {str(e)}"
            }

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        执行获取存储空间列表操作
        
        Args:
            tool_parameters: 工具参数（此工具无需额外参数）
            
        Yields:
            ToolInvokeMessage: 工具执行结果消息
        """
        try:
            # 获取存储空间列表
            list_result = self._list_buckets()
            
            if list_result["success"]:
                # 创建简化的成功消息
                markdown_content = f"存储桶列表获取成功，共 {list_result['count']} 个存储桶"
                
                yield self.create_text_message(markdown_content)
                
                # 成功获取列表
                result = {
                    "buckets": list_result["buckets"],
                    "count": list_result["count"],
                    "error": None
                }
                
                yield self.create_json_message(result)
            else:
                # 创建简化的失败消息
                markdown_content = f"存储桶列表获取失败：{list_result['error']}"
                
                yield self.create_text_message(markdown_content)
                
                # 获取失败，返回错误信息
                result = {
                    "buckets": [],
                    "count": 0,
                    "error": list_result['error']
                }
                yield self.create_json_message(result)
                
        except ToolProviderCredentialValidationError as e:
            # 创建认证错误的简化消息
            markdown_content = f"认证错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 认证错误
            result = {
                "buckets": [],
                "count": 0,
                "error": f"认证错误：{str(e)}"
            }
            yield self.create_json_message(result)
        except Exception as e:
            logger.exception("七牛云存储空间列表工具执行失败")
            
            # 创建通用错误的简化消息
            markdown_content = f"系统错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 其他错误
            result = {
                "buckets": [],
                "count": 0,
                "error": f"执行失败：{str(e)}"
            }
            yield self.create_json_message(result)
