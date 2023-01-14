from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, StrictStr, SecretStr, PrivateAttr
from typing import Annotated, Any
from enum import Enum


class ConnModel(BaseModel, ABC):
    name: Annotated[StrictStr | Enum, Field(allow_mutation=False)]
    password: Annotated[SecretStr, Field(min_length=4)]
    port: Annotated[int, Field(strict=True, ge=1100, le=50000)]
    _test_connection: 'ConnModel' = PrivateAttr(default=None)
    _test_mode: bool = PrivateAttr(default=False)

    class Config:
        validate_assignment = True


class Connection(ConnModel):
    def set_test_connection(self, **kwargs) -> None:
        if 'name' not in kwargs:
            self._test_connection = self.parse_obj(self.dict() | kwargs)
        else:
            raise ValueError(f'Name cannot be set. It is bound to the original connection')

    def remove_test_connection(self) -> None:
        self.set_test_connection()

    def _test(self, enable: bool):
        self._test_mode = enable

    @abstractmethod
    def _connection(self, conn: 'Connection') -> Any:
        ...

    @property
    def connection(self) -> Any:
        if self._test_mode and self._test_connection:
            return self._connection(conn=self._test_connection)
        else:
            return self._connection(conn=self)

    def __eq__(self, other: 'Connection'):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
