from abc import ABC, abstractmethod
from typing import Union

from langchain_groq import ChatGroq

type ReturningClients = Union[ChatGroq, None]


class BaseClient(ABC):
    @abstractmethod
    def create_client(self) -> ReturningClients:
        pass
