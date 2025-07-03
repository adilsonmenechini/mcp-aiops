import logging
import os
import time
from typing import List, Dict, Union

from src.model.llm_clients.base_llm_client import BaseLLMClient
from src.model.llm_clients.gemini_client import GeminiClient
from src.model.llm_clients.ollama_client import OllamaClient
from src.model.llm_clients.anthropic_client import AnthropicClient


class LLMClient:
    """
    Acts as a factory to provide the correct LLM client based on configuration.
    Handles retry logic for LLM calls.
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.client: BaseLLMClient

        if self.provider == "gemini":
            self.client = GeminiClient()
        elif self.provider == "ollama":
            self.client = OllamaClient()
        elif self.provider == "anthropic":
            self.client = AnthropicClient()
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}. "
                             "Please choose 'gemini', 'ollama', or 'anthropic'.")
        logging.info(f"LLMClient initialized with provider: {self.provider}")

        # Parâmetros de retentativa globais
        self.max_retries = int(os.getenv("LLM_MAX_RETRIES", 3))
        self.retry_delay_seconds = float(os.getenv("LLM_RETRY_DELAY_SECONDS", 2.0))

    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Delegates the response generation to the selected LLM client with retry logic.
        Passes additional kwargs (e.g., temperature, max_tokens) to the underlying client.
        """
        for attempt in range(self.max_retries):
            try:
                # Passa todos os kwargs recebidos para o cliente específico do LLM
                response = self.client.get_response(messages, **kwargs)
                if response is not None:
                    return response
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}/{self.max_retries} for LLM response failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay_seconds * (2 ** attempt)) # Exponential backoff
                else:
                    logging.error(f"Max retries reached for LLM response after {self.max_retries} attempts.")
                    return None
        return None