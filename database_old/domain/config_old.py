import sys
import logging
from pathlib import PosixPath
from pydantic import *
from typing import *


NullLogger = logging.getLogger('NULL')
NullLogger.addHandler(logging.NullHandler)

validate_arbitrary_arguments = validate_arguments(config=dict(arbitrary_types_allowed=True))


class ConnConfig(BaseModel):
    _logger: ClassVar[logging.Logger] = Field(NullLogger, alias='logger')
    _instant_client: ClassVar[DirectoryPath | None] = Field(None, alias='instant_client')
    _test_mode: ClassVar[bool] = Field(False, alias='test_mode')

    class Config:
        # allow_mutation = False
        arbitrary_types_allowed = True

    @classmethod
    @validate_arbitrary_arguments
    def _global(cls,
                logger: logging.Logger = NullLogger,
                ora_instant_client: DirectoryPath | None = None,
                test_mode: bool = False):
        cls._logger = logger
        cls._instant_client = ora_instant_client
        cls._test_mode = test_mode

    def _properties(self, include_only: tuple[str] = ()):
        return {k.lstrip('_'): getattr(self, k) for k in self.__class_vars__ if not include_only or k.lstrip('_') in include_only}

    @property
    def properties(self):
        return self._properties()

    @staticmethod
    def enable_testing():
        Cfg.test_mode = True

    @staticmethod
    def disable_testing():
        Cfg.test_mode = False


class NewCfg(Cfg):
    logger: logging.Logger = NullLogger
    instant_client: DirectoryPath | None = None

    @validate_arbitrary_arguments
    def set_locals(self,
                   logger: logging.Logger = NullLogger,
                   instant_client: DirectoryPath | None = None):
        self.logger = logger
        self.instant_client = instant_client

    @property
    def properties(self):
        instance = self.dict()
        return super(NewCfg, self)._properties(instance) | self._properties(instance) | self.dict(exclude_defaults=True)

    # @validator('instant_client')
    # def set_instant_client(cls, value):
    #     if isinstance(value, PosixPath):
    #         return value
    #     else:
    #         print('lolz')




if __name__ == '__main__':
    cfg0, cfg1, cfg2 = Cfg(), NewCfg(), NewCfg()
    # Cfg._global(NullLogger, '/Users')
    # NewCfg.test_mode = True
    cfg2.set_locals(instant_client='/Users/vasilisbardakos')
    print('cfg', cfg0.properties)
    print('new1', cfg1.properties)
    print('new2', cfg2.properties)
    print(NewCfg().__repr_str__(join_str=' | '))
    # print(A.__dict__['_hello'].alias)
    # cfg3.instant_client = 10
    # for cls_var in Cfg.__class_vars__:
    #     print(Cfg.__dict__[cls_var].alias)

