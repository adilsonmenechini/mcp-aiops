from dotenv import load_dotenv
import json
import logging
from typing import Any

class Configuration:
    def __init__(self) -> None:
        self.load_env()

    @staticmethod
    def load_env() -> None:
        load_dotenv()

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        with open(file_path, "r") as f:
            return json.load(f)

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

