import logging
import os
from typing import List, Dict, Union
from src.model.llm_clients.base_llm_client import BaseLLMClient

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage # Adicionado SystemMessage

class AnthropicClient(BaseLLMClient):
    """
    Handles communication with the Anthropic Claude API using LangChain.
    """
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name=os.getenv("ANTHROPIC_MODEL", model_name))
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logging.error("ANTHROPIC_API_KEY environment variable not set.")
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

        logging.info(f"AnthropicClient (LangChain) initialized with model: {self.model_name}")

    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Sends a list of messages to the Anthropic LLM via LangChain and returns its text response.
        Formats messages to be compatible with LangChain's message types.
        Accepts temperature, max_tokens, top_k, top_p via kwargs.
        Handles the system message specifically for Anthropic's API.
        """
        try:
            langchain_messages = []
            system_prompt_content = None

            # Anthropic prefere que o prompt de sistema seja um parâmetro separado.
            # Se a primeira mensagem é um 'model' role (que usamos para o prompt de sistema),
            # extraia seu conteúdo e não a inclua na lista de mensagens normais.
            if messages and messages[0].get("role") == "model":
                system_prompt_content = messages[0]["content"]
                # Processar as mensagens restantes
                for msg in messages[1:]:
                    if msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "model":
                        langchain_messages.append(AIMessage(content=msg["content"]))
                    else:
                        logging.warning(f"Unsupported role in chat history: {msg['role']}. Skipping message.")
            else:
                # Se não houver um prompt de sistema inicial no formato 'model', processe normalmente
                for msg in messages:
                    if msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "model":
                        langchain_messages.append(AIMessage(content=msg["content"]))

            # Mapear kwargs para parâmetros do ChatAnthropic
            llm_params = {
                "temperature": kwargs.get("temperature", float(os.getenv("LLM_TEMPERATURE", 0.5))),
                "max_tokens": kwargs.get("max_tokens", int(os.getenv("LLM_MAX_TOKENS", 4096))),
                "top_k": kwargs.get("top_k", int(os.getenv("LLM_TOP_K", 2))),
                "top_p": kwargs.get("top_p", float(os.getenv("LLM_TOP_P", 0.5))),
                # Outros parâmetros Anthropic podem ser adicionados aqui
            }

            llm = ChatAnthropic(
                anthropic_api_key=self.api_key,
                model=self.model_name,
                **llm_params
            )

            # Passar o system_prompt_content como o argumento 'system' se existir
            response_kwargs = {}
            if system_prompt_content:
                response_kwargs["system"] = system_prompt_content

            response = llm.invoke(langchain_messages, **response_kwargs)
            return response.content
        except Exception as e:
            logging.error(f"Error with Anthropic model {self.model_name} (LangChain): {e}")
            return None