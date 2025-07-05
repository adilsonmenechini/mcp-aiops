import logging
import os
from typing import List, Dict, Union
from src.model.llm_clients.base_llm_client import BaseLLMClient

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class AnthropicClient(BaseLLMClient):
    """
    Handles communication with the Anthropic Claude API using LangChain.
    Based on the working implementation from ui-streamlit/services/ai_service.py
    """
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name=os.getenv("ANTHROPIC_MODEL", model_name))
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logging.error("ANTHROPIC_API_KEY environment variable not set.")
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

        logging.info(f"AnthropicClient (LangChain) initialized with model: {self.model_name}")

    def _create_llm_instance(self, **kwargs) -> ChatAnthropic:
        """Create a ChatAnthropic instance with the given parameters."""
        return ChatAnthropic(
            anthropic_api_key=self.api_key,
            model=self.model_name,
            temperature=kwargs.get("temperature", float(os.getenv("LLM_TEMPERATURE", 0.5))),
            max_tokens=kwargs.get("max_tokens", int(os.getenv("LLM_MAX_TOKENS", 4096))),
            # Note: top_k and top_p are not standard parameters for ChatAnthropic
            # They will be ignored if not supported
        )

    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, None]:
        """
        Sends a list of messages to the Anthropic LLM via LangChain and returns its text response.
        Uses the same pattern as the working ui-streamlit implementation.
        """
        try:
            langchain_messages = []
            system_prompt_content = None

            # Extract system message if present (first message with role 'model')
            if messages and messages[0].get("role") == "model":
                system_prompt_content = messages[0]["content"]
                messages_to_process = messages[1:]
                logging.debug(f"AnthropicClient - Extracted system prompt: {len(system_prompt_content)} chars")
            else:
                messages_to_process = messages
                logging.debug("AnthropicClient - No system prompt found")

            # Add system message first if present
            if system_prompt_content:
                langchain_messages.append(SystemMessage(content=system_prompt_content))

            # Convert remaining messages to LangChain format
            for msg in messages_to_process:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "model":
                    langchain_messages.append(AIMessage(content=msg["content"]))
                else:
                    logging.warning(f"AnthropicClient - Unsupported role: {msg['role']}. Skipping message.")

            # Log message composition
            logging.debug(f"AnthropicClient - Composed {len(langchain_messages)} messages")
            for i, msg in enumerate(langchain_messages):
                logging.debug(f"AnthropicClient - Message {i}: {type(msg).__name__} ({len(msg.content)} chars)")

            # Create LLM instance with parameters
            llm = self._create_llm_instance(**kwargs)
            
            # Log parameters being used
            logging.debug(f"AnthropicClient - Using parameters: temperature={kwargs.get('temperature', 0.5)}, max_tokens={kwargs.get('max_tokens', 4096)}")

            # Invoke the model
            logging.debug("AnthropicClient - Invoking LLM...")
            response = llm.invoke(langchain_messages)
            
            logging.debug(f"AnthropicClient - Response received: {len(response.content) if response.content else 0} characters")
            logging.debug(f"AnthropicClient - Response preview: {response.content[:100] if response.content else 'None'}...")
            
            return response.content
            
        except Exception as e:
            logging.error(f"AnthropicClient - Error with model {self.model_name}: {e}")
            logging.error(f"AnthropicClient - Exception details: {type(e).__name__}: {str(e)}")
            return None
