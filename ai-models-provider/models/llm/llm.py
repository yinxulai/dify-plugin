from collections.abc import Generator
from typing import Optional, Union
from dify_plugin.entities.model.llm import LLMMode, LLMResult
from dify_plugin.entities.model.message import PromptMessage, PromptMessageTool
from yarl import URL
from dify_plugin import OAICompatLargeLanguageModel


class QiniuLargeLanguageModel(OAICompatLargeLanguageModel):
    """
    七牛云大语言模型实现类
    基于 OpenAI 兼容接口实现，支持多种七牛云 AI 模型
    """

    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: Optional[list[PromptMessageTool]] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[LLMResult, Generator]:
        """
        调用七牛云大语言模型

        Args:
            model: 模型名称
            credentials: 认证信息
            prompt_messages: 提示消息列表
            model_parameters: 模型参数
            tools: 工具列表（可选）
            stop: 停止词列表（可选）
            stream: 是否流式返回
            user: 用户标识（可选）

        Returns:
            LLMResult 或 Generator
        """
        self._add_custom_parameters(credentials)
        
        # 对于自定义模型，model 参数已经是用户输入的模型名称
        # 不需要额外处理，直接使用即可
        
        return super()._invoke(model, credentials, prompt_messages, model_parameters, tools, stop, stream, user)

    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        验证认证信息

        Args:
            model: 模型名称
            credentials: 认证信息
        """
        self._add_custom_parameters(credentials)
        
        # 对于自定义模型，model 参数已经是用户输入的模型名称
        # 不需要额外处理，直接使用即可
        
        super().validate_credentials(model, credentials)

    @staticmethod
    def _add_custom_parameters(credentials: dict) -> None:
        """
        添加七牛云特定的参数

        Args:
            credentials: 认证信息字典
        """
        credentials["endpoint_url"] = str(URL(credentials.get("endpoint_url", "https://openai.qiniu.com/v1")))
        credentials["mode"] = LLMMode.CHAT.value
        credentials["function_calling_type"] = "tool_call"
        credentials["stream_function_calling"] = "support"
