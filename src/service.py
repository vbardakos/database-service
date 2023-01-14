from enum import Enum


class DatabaseService:
    def __init__(self, name: str | Enum):
        self._adapter = None

    @classmethod
    def register(cls): ...