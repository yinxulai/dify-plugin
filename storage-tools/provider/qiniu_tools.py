import logging
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from qiniu import Auth, BucketManager

logger = logging.getLogger(__name__)


class QiniuProvider(ToolProvider):
    """
    七牛云工具提供商实现类
    
    提供七牛云存储工具能力，支持文件上传功能
    """

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证工具认证信息（用于工具服务）
        验证七牛云 Access Key 和 Secret Key 的有效性
        
        Args:
            credentials: 认证信息字典，包含 qiniu_access_key 和 qiniu_secret_key
            
        Raises:
            ToolProviderCredentialValidationError: 认证验证失败
        """
        try:
            access_key = credentials.get("qiniu_access_key")
            secret_key = credentials.get("qiniu_secret_key")
            
            if not access_key or not secret_key:
                raise ToolProviderCredentialValidationError("七牛云 Access Key 和 Secret Key 不能为空")
            
            # 创建认证对象
            auth = Auth(access_key, secret_key)
            bucket_manager = BucketManager(auth)
            
            # 尝试获取空间列表来验证认证信息
            # 这里只是验证认证是否有效，不需要具体的空间名
            try:
                # 调用接口验证认证信息
                ret, info = bucket_manager.buckets()
                
                if info.status_code == 200:
                    logger.info("七牛云认证验证成功")
                elif info.status_code == 401:
                    raise ToolProviderCredentialValidationError("七牛云认证失败，请检查 Access Key 和 Secret Key 是否正确")
                else:
                    raise ToolProviderCredentialValidationError(f"七牛云认证验证失败: HTTP {info.status_code}")
                    
            except Exception as api_error:
                if "401" in str(api_error) or "Unauthorized" in str(api_error):
                    raise ToolProviderCredentialValidationError("七牛云认证失败，请检查 Access Key 和 Secret Key 是否正确")
                else:
                    # 网络错误等其他错误也应该抛出异常，不能跳过验证
                    logger.error(f"七牛云认证验证时出现错误: {str(api_error)}")
                    raise ToolProviderCredentialValidationError(f"认证验证失败: {str(api_error)}")
                    
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            logger.exception("七牛云认证验证过程中发生未知错误")
            raise ToolProviderCredentialValidationError(f"认证验证失败: {str(e)}")
