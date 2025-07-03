import logging
import os
from typing import List, Dict, Union
from src.model.llm_clients.base_llm_client import BaseLLMClient

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage # Adicionado SystemMessage

class GeminiClient(BaseLLMClient):
    """
    Handles communication with the Google Gemini API using LangChain.
    """
    def __init__(self, model_name: str = "gemini-pro"):
        super().__init__(model_name=os.getenv("GOOGLE_MODEL", model_name))
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logging.error("GOOGLE_API_KEY environment variable not set.")
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        # O LLM será instanciado no get_response para permitir flexibilidade de parâmetros
        logging.info(f"GeminiClient (LangChain) initialized with model: {self.model_name}")

    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Sends a list of messages to the Gemini LLM via LangChain and returns its text response.
        Formats messages to be compatible with LangChain's message types.
        Accepts temperature, max_tokens (as max_output_tokens), top_k, top_p via kwargs.
        """
        try:
            # Extrair o prompt de sistema se existir na primeira mensagem e for do role 'model'
            # Gemini pode aceitar a mensagem de sistema como parte da lista de mensagens
            # ou como um parâmetro SystemMessage. Vamos converter o 'model' inicial em SystemMessage.
            langchain_messages = []
            if messages and messages[0].get("role") == "model":
                # Assumimos que o primeiro 'model' role é o prompt do sistema
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

            # Mapear kwargs para parâmetros do ChatGoogleGenerativeAI
            llm_params = {
                "temperature": kwargs.get("temperature", float(os.getenv("LLM_TEMPERATURE", 0.5))),
                "max_output_tokens": kwargs.get("max_tokens", int(os.getenv("LLM_MAX_TOKENS", 4096))),
                "top_k": kwargs.get("top_k", int(os.getenv("LLM_TOP_K", 2))),
                "top_p": kwargs.get("top_p", float(os.getenv("LLM_TOP_P", 0.5))),
                "max_retries": kwargs.get("max_retries", 2), # Exemplo de parâmetro específico do Gemini
            }

            llm = ChatGoogleGenerativeAI(
                google_api_key=self.api_key,
                model=self.model_name,
                **llm_params
            )

            response = llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            logging.error(f"Error with Gemini model {self.model_name} (LangChain): {e}")
            return None