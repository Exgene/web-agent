import os
from logging import INFO

import dotenv
from groq import AsyncGroq, Groq

from src.clients.base import AsyncGroqReturnType, BaseClient, SyncGroqReturnType
from src.logger.logger import get_logger, setup_logger

setup_logger("groq_client", INFO)
dotenv.load_dotenv(".env")
logger = get_logger("groq_client")
API_KEY = os.environ.get("GROQ_API_KEY")

if API_KEY is None:
    assert "MISSING API KEYS"

logger.info(API_KEY)


class GroqClient(BaseClient):
    def __init__(self):
        self.llm = None

    def create_sync_client(self) -> SyncGroqReturnType:
        self.llm = Groq(
            api_key=API_KEY,
        )
        logger.debug("Successfully created Groq Client")
        model = "llama3-8b-8192"
        return self.llm, model

    def create_async_client(self) -> AsyncGroqReturnType:
        self.llm = AsyncGroq(api_key=API_KEY)
        logger.debug("Successfully created Groq Client")
        model = "llama3-8b-8192"
        return self.llm, model
