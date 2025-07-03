import json
import streamlit as st

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from typing import Optional, Any, Union
from config import MODEL_OPTIONS


def create_llm_model(llm_provider: str, **kwargs) -> Union[ChatOpenAI, ChatAnthropic, ChatOllama, ChatGoogleGenerativeAI]:
    """Create a language model based on the selected provider.
    
    Args:
        llm_provider (str): The name of the LLM provider to use ('OpenAI', 'Antropic', 'Ollama', 'Google')
        **kwargs: Additional keyword arguments for model configuration
            - temperature (float): Controls randomness in responses (0.0 to 1.0)
            - max_tokens (int): Maximum length of generated response
            - streaming (bool): Whether to stream the response
    
    Returns:
        Union[ChatOpenAI, ChatAnthropic, ChatOllama, ChatGoogleGenerativeAI]: An initialized chat model instance
        
    Raises:
        ValueError: If an unsupported LLM provider is specified
    """
    params = st.session_state.get('params')

    if llm_provider == "OpenAI":
        return ChatOpenAI(
            openai_api_key=params.get("api_key"),
            model=MODEL_OPTIONS['OpenAI'],
            temperature=kwargs.get('temperature', 0.7),
        )
    elif llm_provider == "Antropic":
        return ChatAnthropic(
            anthropic_api_key=params.get("api_key"),
            model=MODEL_OPTIONS['Antropic'],
            temperature=kwargs.get('temperature', 0.7),
        )
    elif llm_provider == "Ollama":
        return ChatOllama(
            model=MODEL_OPTIONS['Ollama'],
            temperature=kwargs.get('temperature', 0.7),
            max_tokens=kwargs.get('max_tokens', 4096),
            streaming=kwargs.get('streaming', False),
        )
    elif llm_provider == "Google":
        return ChatGoogleGenerativeAI(
            google_api_key=params.get("api_key"),
            model=MODEL_OPTIONS['Google'],
            temperature=kwargs.get('temperature', 0.7),
            max_tokens=kwargs.get('max_tokens', 4096),
            max_retries=2,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")


def get_response(prompt: str, llm_provider: str) -> str:
    """Get a response from the LLM using the standard LangChain interface.
    
    Args:
        prompt (str): The input text prompt to send to the model
        llm_provider (str): The name of the LLM provider to use
    
    Returns:
        str: The model's response text, or an error message if the invocation fails
    """
    try:
        # Create the LLM instance dynamically
        llm = create_llm_model(llm_provider)

        # Wrap prompt in a HumanMessage
        message = HumanMessage(content=prompt)

        # Invoke model and return the output content
        response = llm.invoke([message])
        return response.content

    except Exception as e:
        return f"Error during LLM invocation: {str(e)}"


def get_response_stream(
    prompt: str,
    llm_provider: str,
    system: Optional[str] = '',
    temperature: float = 1.0,
    max_tokens: int = 4096,
    **kwargs,
) -> Any:
    """Get a streaming response from the selected LLM provider.
    All provider-specific connection/auth should be handled via kwargs.
    
    Args:
        prompt (str): The input text prompt to send to the model
        llm_provider (str): The name of the LLM provider to use
        system (Optional[str]): System message to prepend to the conversation
        temperature (float): Controls randomness in responses (0.0 to 1.0)
        max_tokens (int): Maximum length of generated response
        **kwargs: Additional provider-specific parameters
    
    Returns:
        Any: A streaming response iterator from the LLM
        
    Raises:
        Exception: If there is an error during streaming, displays error in Streamlit UI
    """
    try:
        # Add streaming and generation params to kwargs
        kwargs.update({
            "temperature": temperature,
            "max_tokens": max_tokens,
            "streaming": True
        })

        # Create the LLM with streaming enabled
        llm = create_llm_model(llm_provider, **kwargs)

        # Compose messages
        messages = []
        if system:
            messages.append(SystemMessage(content=system))
        messages.append(HumanMessage(content=prompt))

        # Stream the response
        stream_response = llm.stream(messages)
        return stream_response
    except Exception as e:
        st.error(f"[Error during streaming: {str(e)}]")
        st.stop()