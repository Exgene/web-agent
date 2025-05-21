from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import CoroutineType
from typing import Any, Union

from groq.types.chat import ChatCompletion

from src.clients.base import AsyncClientTypes, SyncClientTypes
from src.logger.logger import setup_logger

type LLMType = Union[AsyncClientTypes, SyncClientTypes]
type SyncAgentReturnType = Union[ChatCompletion, None]
type AsyncAgentReturnType = Union[CoroutineType[Any, Any, ChatCompletion], None]

setup_logger("agent_base")


@dataclass
class BaseAgent(ABC):
    input: str
    llm: LLMType
    memory: str
    model: str
    outputs: list[dict[str, Any]]

    @abstractmethod
    def run(self) -> SyncAgentReturnType:
        pass

    @abstractmethod
    async def async_run(self) -> AsyncAgentReturnType:
        pass
