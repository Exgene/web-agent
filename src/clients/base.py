from abc import ABC, abstractmethod
from typing import Union

from groq import Groq

type ReturningClients = Union[Groq, None]


class BaseClient(ABC):
    @abstractmethod
    def create_client(self) -> ReturningClients:
        pass
