from abc import ABC, abstractmethod
from typing import List, Dict, Union

class BaseLLMClient(ABC):
    """
    Abstract base class for all LLM clients.
    Defines the interface for interacting with different LLM providers.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Sends a list of messages to the LLM and returns its text response.
        Allows passing additional configuration parameters via kwargs.
        """
        pass