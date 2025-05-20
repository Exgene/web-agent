from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from src.clients.base import AsyncClientTypes, SyncClientTypes

type LLMType = Union[AsyncClientTypes, SyncClientTypes]


@dataclass
class BaseAgent(ABC):
    input: str
    llm: LLMType

    @abstractmethod
    def run(self):
        pass
