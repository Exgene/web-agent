from abc import ABC, abstractmethod
from typing import Dict, Union

from groq import Groq

type GroqClient = Dict[str, Groq | str]

type ReturningClients = Union[GroqClient, None]


class BaseClient(ABC):
    @abstractmethod
    def create_client(self) -> ReturningClients:
        pass
