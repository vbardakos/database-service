from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def ping(self): ...

    @property
    @abstractmethod
    def connection_info(self) -> dict: ...

