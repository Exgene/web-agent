import os
from logging import INFO

import dotenv
from langchain_groq import ChatGroq

from src.clients.base import BaseClient
from src.logger.logger import get_logger, setup_logger

dotenv.load_dotenv(".env")
setup_logger("groq_client", INFO)
logger = get_logger("groq_client")


if "GROQ_API_KEY" not in os.environ:
    assert "MISSING API KEYS"


class GroqClient(BaseClient):
    def __init__(self):
        self.llm = None

    def create_client(self) -> ChatGroq:
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
        )
        logger.debug("Successfully created Groq Client")
        return self.llm
