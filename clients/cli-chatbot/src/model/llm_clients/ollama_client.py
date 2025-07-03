import logging
import os
from typing import List, Dict, Union
from src.model.llm_clients.base_llm_client import BaseLLMClient

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage # Adicionado SystemMessage

class OllamaClient(BaseLLMClient):
    """
    Handles communication with a local Ollama instance using LangChain.
    """
    def __init__(self, model_name: str = "llama2"):
        super().__init__(model_name=os.getenv("OLLAMA_MODEL", model_name))
        self.base_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")

        logging.info(f"OllamaClient (LangChain) initialized with model: {self.model_name} at {self.base_url}")

    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Sends a list of messages to the Ollama LLM via LangChain and returns its text response.
        Formats messages to be compatible with LangChain's message types.
        Accepts temperature, max_tokens (as num_predict), top_k, top_p via kwargs.
        """
        try:
            langchain_messages = []
            if messages and messages[0].get("role") == "model":
                # Para Ollama, o SystemMessage é bem suportado.
                langchain_messages.append(SystemMessage(content=messages[0]["content"]))
                for msg in messages[1:]:
                    if msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "model":
                        langchain_messages.append(AIMessage(content=msg["content"]))
            else:
                for msg in messages:
                    if msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "model":
                        langchain_messages.append(AIMessage(content=msg["content"]))

            # Mapear kwargs para parâmetros do ChatOllama
            llm_params = {
                "temperature": kwargs.get("temperature", float(os.getenv("LLM_TEMPERATURE", 0.5))),
                "num_predict": kwargs.get("max_tokens", int(os.getenv("LLM_MAX_TOKENS", 4096))), # Ollama usa num_predict
                "top_k": kwargs.get("top_k", int(os.getenv("LLM_TOP_K", 2))),
                "top_p": kwargs.get("top_p", float(os.getenv("LLM_TOP_P", 0.5))),
                "base_url": self.base_url, # Usar a URL base configurada
            }

            llm = ChatOllama(
                model=self.model_name,
                **llm_params
            )

            response = llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            logging.error(f"Error with Ollama model {self.model_name} at {self.base_url} (LangChain): {e}")
            return None