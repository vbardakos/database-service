from abc import ABC, abstractmethod
from typing import *
# from ctypes import c_uint8


class DbConnector(ABC):

    @property
    @abstractmethod
    def info(self): ...


if __name__ == '__main__':
    from typing import Callable
    from pydantic import *
    from pydantic import types


    class _MetaCHARVAR(type):
        def __getitem__(self, item):
            return constr(max_length=item)


    class VARCHAR(metaclass=_MetaCHARVAR):
        ...


    class A(BaseModel):
        x: VARCHAR[2]

    print(A(x='ac'))

