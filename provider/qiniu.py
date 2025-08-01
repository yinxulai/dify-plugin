import logging
from dify_plugin.entities.model import ModelType
from dify_plugin.errors.model import CredentialsValidateFailedError
from dify_plugin import ModelProvider

logger = logging.getLogger(__name__)


class QiniuProvider(ModelProvider):
    """
    七牛云模型提供商实现类
    
    提供七牛云 AI 模型的接入能力，支持多种大语言模型
    """

    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        验证供应商认证信息
        如果验证失败，会抛出异常

        Args:
            credentials: 供应商认证信息，格式由 `provider_credential_schema` 定义

        Raises:
            CredentialsValidateFailedError: 认证验证失败
        """
        try:
            model_instance = self.get_model_instance(ModelType.LLM)
            # 使用 deepseek-v3 作为默认验证模型
            model_instance.validate_credentials(model="deepseek-v3", credentials=credentials)
        except CredentialsValidateFailedError as ex:
            raise ex
        except Exception as ex:
            logger.exception(f"{self.get_provider_schema().provider} credentials validate failed")
            raise ex
