from abc import ABC, abstractmethod
from typing import Callable

from service.domain.settings import BaseConnectionSettings, ExtraSettings
from service.domain.types import SchemaPyObject


class BaseAdapter(ABC):
    def __init__(self, name: str):
        self._name = name
        self._dsn = None
        self._log = None
        self._arg = None

    def __call__(self, connection: BaseConnectionSettings):
        self._dsn: str = self._get_dsn(connection)
        self._log: object = connection.extras.logging_object(self._name)
        self._arg: ExtraSettings = connection.extras
        return self

    @abstractmethod
    def _get_dsn(self, conn: BaseConnectionSettings):
        ...

    @abstractmethod
    def _execute(self, stmt: str, fetch: int, fetchall: bool, commit: bool, row_factory: Callable):
        ...
