from dotenv import load_dotenv
import json
import logging
import os
from typing import Any, Dict

class Configuration:
    def __init__(self) -> None:
        self.load_env()
        self.llm_config_params = self.load_llm_config()

    @staticmethod
    def load_env() -> None:
        load_dotenv()

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def load_llm_config() -> Dict[str, Any]:
        """Carrega e valida os parâmetros de configuração do LLM a partir de variáveis de ambiente."""
        try:
            params = {
                "temperature": float(os.getenv("LLM_TEMPERATURE", 0.5)),
                "max_tokens": int(os.getenv("LLM_MAX_TOKENS", 4096)),
                "top_k": int(os.getenv("LLM_TOP_K", 2)),
                "top_p": float(os.getenv("LLM_TOP_P", 0.5)),
            }
            logging.info(f"Parâmetros de configuração do LLM carregados: {params}")
            return params
        except (ValueError, TypeError) as e:
            logging.error(f"Erro ao carregar configuração do LLM: {e}. Usando valores padrão.")
            # Retorna padrões seguros em caso de erro
            return {"temperature": 0.5, "max_tokens": 4096, "top_k": 2, "top_p": 0.5}

class LogLevel:
    # Configure logging
    @staticmethod
    def configure_logging(log_level: str = "INFO") -> None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        logging.basicConfig(level=numeric_level, format="%(asctime)s - %(levelname)s - %(message)s")

sre_system_prompt = """
    Você é um assistente SRE especializado. Concentre-se em confiabilidade, desempenho, e resposta a incidentes. Priorize a estabilidade do sistema e a automação de tarefas repetitivas.
    
    Ao exibir informações sobre ferramentas:
    1. Evite duplicação de conteúdo
    2. Mantenha a formatação consistente
    3. Apresente cada ferramenta apenas uma vez
    4. Seja conciso nas descrições
"""
