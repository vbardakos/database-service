from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Union, Callable, Optional, Iterable
from src._domain.conn_validator import ConnValidator


class BaseConnection(ABC):
    def __init__(self, obj: Union[dict, ]):
        self.validator = ConnValidator(self._schema)
        self._conn, self._kwargs = self._split_validated_schema(params)

    @abstractmethod
    def _connection(self, apply: Callable, apply_kwargs: dict, factory: Callable, fetch: int = 0) -> Optional[Iterable]:
        """
        :param
        apply:          inside cursor function
        apply_kwargs:   apply params
        factory:        after cursor function
        fetch:          fetch rows. use -1 for fetchall
        """
        ...

    @abstractmethod
    async def _async_connection(self, apply: Callable, factory: Callable, commit: bool,
                                fetch: int, fetchall: bool, as_type: type, **kwargs): ...

    def _split_validated_schema(self, kwargs: dict):
        if self.validator.validate(kwargs):
            return self.validator.normalized_with_remainder(kwargs)
        else:
            raise Exception('nope!')

    @property
    @abstractmethod
    def _schema(self) -> dict: ...
