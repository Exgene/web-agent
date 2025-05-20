import os
from logging import INFO

from groq import Groq

from src.clients.base import BaseClient
from src.clients.base import GroqClient as GroqReturnType
from src.logger.logger import get_logger, setup_logger

setup_logger("groq_client", INFO)
logger = get_logger("groq_client")
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    assert "MISSING API KEYS"


class GroqClient(BaseClient):
    def __init__(self):
        self.llm = None

    def create_client(self) -> GroqReturnType:
        self.llm = Groq(
            api_key=API_KEY,
        )
        logger.debug("Successfully created Groq Client")
        model = "llama3-8b-8192"
        return {"llm": self.llm, "model": model}
