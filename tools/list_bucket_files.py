import json
import logging
from collections.abc import Generator
from typing import Any

from qiniu import Auth, BucketManager
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

logger = logging.getLogger(__name__)


class QiniuListFilesTool(Tool):
    """
    七牛云文件列表工具
    
    根据前缀列出指定存储空间中的文件
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

    def _list_files(self, bucket: str, prefix: str = None, limit: int = 100, marker: str = None) -> dict:
        """列出文件"""
        try:
            auth = self._get_auth()
            bucket_manager = BucketManager(auth)
            
            # 获取文件列表
            ret, eof, info = bucket_manager.list(
                bucket, 
                prefix=prefix, 
                marker=marker, 
                limit=limit
            )
            
            if info.status_code == 200:
                files = []
                next_marker = None
                
                if ret:
                    # 根据官方文档，响应应该包含 items 字段和可选的 marker 字段
                    if isinstance(ret, dict):
                        # 标准响应格式：包含 items 和 marker
                        items = ret.get("items", [])
                        next_marker = ret.get("marker", None)
                    else:
                        logger.warning(f"意外的返回数据类型: {type(ret)} - {ret}")
                        items = []
                    
                    # 处理文件条目
                    for item in items:
                        # 确保 item 是字典类型
                        if isinstance(item, dict):
                            file_info = {
                                "key": item.get("key", ""),
                                "size": item.get("fsize", 0),
                                "hash": item.get("hash", ""),
                                "put_time": item.get("putTime", 0),
                                "last_modify": item.get("lastModify", item.get("putTime", 0)),
                                "mime_type": item.get("mimeType", ""),
                                "end_user": item.get("endUser", ""),
                                "type": item.get("type", 0),
                                "status": item.get("status", 0),
                                "md5": item.get("md5", "")
                            }
                            files.append(file_info)
                        else:
                            # 如果 item 不是字典，记录警告并跳过
                            logger.warning(f"跳过非字典类型的文件项: {type(item)} - {item}")
                
                # 如果没有从响应中获取到 marker，尝试从最后一个文件的 key 生成
                if next_marker is None and files:
                    next_marker = files[-1].get("key")
                
                return {
                    "success": True,
                    "files": files,
                    "count": len(files),
                    "eof": eof,  # 是否已经到了最后一页
                    "marker": next_marker  # 下一页的标记
                }
            elif info.status_code == 401:
                raise ToolProviderCredentialValidationError("七牛云认证失败，请检查 Access Key 和 Secret Key")
            elif info.status_code == 631:
                raise ToolProviderCredentialValidationError(f"存储空间 '{bucket}' 不存在")
            else:
                return {
                    "success": False,
                    "error": f"获取文件列表失败: HTTP {info.status_code} - {info.error if hasattr(info, 'error') else ''}"
                }
                
        except Exception as e:
            if isinstance(e, ToolProviderCredentialValidationError):
                raise
            return {
                "success": False,
                "error": f"获取文件列表时发生错误: {str(e)}"
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
        执行获取文件列表操作
        
        Args:
            tool_parameters: 工具参数，包含 bucket, prefix(可选), limit(可选), marker(可选), domain(可选)
            
        Yields:
            ToolInvokeMessage: 工具执行结果消息
        """
        try:
            # 获取参数
            bucket = tool_parameters.get("bucket", "")
            prefix = tool_parameters.get("prefix", "")
            limit = tool_parameters.get("limit", 100)
            marker = tool_parameters.get("marker", "")
            domain = tool_parameters.get("domain", "")
            
            # 验证必需参数
            if not bucket:
                yield self.create_text_message("存储空间名称不能为空")
                return

            # 参数处理
            if prefix == "":
                prefix = None
            if marker == "":
                marker = None
            
            # 限制 limit 范围
            limit = max(1, min(limit, 1000))  # 限制在 1-1000 之间

            # 验证存储空间访问权限
            self._validate_bucket_access(bucket)
            
            # 执行文件列表获取
            list_result = self._list_files(bucket, prefix, limit, marker)
            
            if list_result["success"]:
                # 为文件添加访问链接
                files_with_urls = []
                for file_info in list_result["files"]:
                    file_with_url = file_info.copy()
                    if domain:
                        file_with_url["url"] = self._generate_access_url(
                            file_info["key"], 
                            bucket, 
                            domain
                        )
                    else:
                        file_with_url["url"] = None
                    files_with_urls.append(file_with_url)
                
                # 创建简化的成功消息
                markdown_content = f"文件列表获取成功，共 {list_result['count']} 个文件"
                
                yield self.create_text_message(markdown_content)
                
                # 成功获取列表
                result = {
                    "files": files_with_urls,
                    "count": list_result["count"],
                    "eof": list_result["eof"],
                    "next_marker": list_result["marker"] if not list_result["eof"] else None,
                    "bucket": bucket,
                    "prefix": prefix,
                    "error": None
                }
                
                yield self.create_json_message(result)
            else:
                # 创建简化的失败消息
                markdown_content = f"文件列表获取失败：{list_result['error']}"
                
                yield self.create_text_message(markdown_content)
                
                # 获取失败，返回错误信息
                result = {
                    "files": [],
                    "count": 0,
                    "eof": True,
                    "next_marker": None,
                    "bucket": bucket,
                    "prefix": prefix,
                    "error": list_result['error']
                }
                yield self.create_json_message(result)
                
        except ToolProviderCredentialValidationError as e:
            # 创建认证错误的简化消息
            markdown_content = f"认证错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 认证错误
            result = {
                "files": [],
                "count": 0,
                "eof": True,
                "next_marker": None,
                "bucket": bucket if 'bucket' in locals() else "",
                "prefix": prefix if 'prefix' in locals() else "",
                "error": f"认证错误：{str(e)}"
            }
            yield self.create_json_message(result)
        except Exception as e:
            logger.exception("七牛云文件列表工具执行失败")
            
            # 创建通用错误的简化消息
            markdown_content = f"系统错误：{str(e)}"
            
            yield self.create_text_message(markdown_content)
            
            # 其他错误
            result = {
                "files": [],
                "count": 0,
                "eof": True,
                "next_marker": None,
                "bucket": bucket if 'bucket' in locals() else "",
                "prefix": prefix if 'prefix' in locals() else "",
                "error": f"执行失败：{str(e)}"
            }
            yield self.create_json_message(result)
