from langchain.chat_models.openai import ChatOpenAI

from chatgpt_wrapper.core.provider import Provider, PresetValue

class CustomChatOpenAI(ChatOpenAI):
    @property
    def _llm_type(self):
        """Return type of llm."""
        return "chat_openai"

    def dict(self, **kwargs):
        """Return a dictionary of the LLM."""
        starter_dict = dict(self._identifying_params)
        starter_dict["_type"] = self._llm_type
        return starter_dict

class ProviderChatOpenai(Provider):

    @property
    def capabilities(self):
        return {
            'streaming': True,
            'models': {
                'gpt-3.5-turbo': {
                    'max_tokens': 4096,
                },
                'gpt-3.5-turbo-0301': {
                    'max_tokens': 4096,
                },
                'gpt-4': {
                    'max_tokens': 8192,
                },
                'gpt-4-0314': {
                    'max_tokens': 8192,
                },
                'gpt-4-32k': {
                    'max_tokens': 32768,
                },
                'gpt-4-32k-0314': {
                    'max_tokens': 32768,
                },
            }
        }

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return CustomChatOpenAI

    def customization_config(self):
        return {
            'verbose': PresetValue(bool),
            'model_name': PresetValue(str, options=self.capabilities['models'].keys()),
            'temperature': PresetValue(float, min_value=0.0, max_value=2.0),
            'model_kwargs': dict,
            'openai_api_key': PresetValue(str, include_none=True, private=True),
            'openai_organization': PresetValue(str, include_none=True, private=True),
            'request_timeout': PresetValue(int),
            'max_retries': PresetValue(int, 1, 10),
            'streaming': PresetValue(bool),
            'n': PresetValue(int, 1, 10),
            'max_tokens': PresetValue(int, include_none=True),
        }
