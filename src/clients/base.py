from abc import ABC, abstractmethod
from typing import Tuple, Union

from groq import AsyncGroq, Groq

type SyncGroqReturnType = Tuple[Groq, str]
type AsyncGroqReturnType = Tuple[AsyncGroq, str]

type SyncClientReturnTypes = Union[SyncGroqReturnType, None]
type AsyncClientReturnTypes = Union[AsyncGroqReturnType, None]

type SyncClientTypes = Union[Groq, None]
type AsyncClientTypes = Union[AsyncGroq, None]


class BaseClient(ABC):
    @abstractmethod
    def create_sync_client(self) -> SyncClientReturnTypes:
        pass

    @abstractmethod
    def create_async_client(self) -> AsyncClientReturnTypes:
        pass
