from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from src.logger.logger import setup_logger
from src.clients.base import AsyncClientTypes, SyncClientTypes

type LLMType = Union[AsyncClientTypes, SyncClientTypes]

setup_logger("agent_base")

@dataclass
class BaseAgent(ABC):
    input: str
    llm: LLMType
    memory: str
    model: str

    @abstractmethod
    def run(self):
        pass
