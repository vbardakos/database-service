import oracledb
from pydantic import StrictStr, StrictInt, AnyHttpUrl, DirectoryPath, validate_arguments, BaseModel, validator
from database.domain.connection_old import Connection
from typing import Any, Annotated, ClassVar


class ORAConnection(Connection):
    database: StrictStr
    host: StrictStr | AnyHttpUrl
    user: StrictStr
    port: StrictInt = 1521
    encoding: StrictStr = 'UTF-8'
    _lib: ClassVar[DirectoryPath]
    _set: ClassVar[bool] = False

    @classmethod
    @validate_arguments
    def set_instant_client(cls, path: DirectoryPath):
        cls._lib = path

    @classmethod
    def parse_with_dsn(cls, *, name: str, user: str, password: str, dsn: str, encoding: str = 'UTF-8'):
        rdy_params = dict(name=name, password=password, user=user, encoding=encoding)
        dsn_params = cls._params_from_dsn(dsn)
        return cls(**rdy_params, **dsn_params)

    def _connection(self, conn: 'ORAConnection') -> tuple:
        return dict(user=self.user, password=self.password.get_secret_value(), dsn=self.dsn, encoding=self.encoding)

    @classmethod
    def _params_from_dsn(cls, dsn_string: str):
        full_host, _, database = dsn_string.partition('/')
        host, _, port = full_host.partition(':')
        return dict(host=host, database=database, port=int(port or cls.__fields__['port'].default))

    @property
    def dsn(self):
        return oracledb.makedsn(self.host, self.port, service_name=self.database)


if __name__ == '__main__':
    # ORAConnection.set_instant_client(path='/Users/vasilisbardakos/Downloads/instantclient_19_8')
    # ora = ORAConnection.parse_with_dsn(name='ora', password='1234', user='user', dsn='abc:1234/abc')
    # print(ora._lib)
    # ORAConnection.set_instant_client(path='/Users/vasilisbardakos/Downloads')
    # print(ora._lib)
    class A(BaseModel):
        _x: ClassVar[bool] = False

        def __init__(self, *args, **kwargs):
            if not self._x:
                print('initialize')
                A._x = True
            super(A, self).__init__(*args, **kwargs)

    class B(A):
        y: str = None

        @validator('y')
        def set_y(cls, v):
            return v * 2 if v == 'abc' else v

    print(B(y='abc'))


# import sys
# import logging
# import cx_Oracle
# from src.main.environment import InstantClientCfg
#
#
# class ClientInitializer(type):
#     """
#     Oracle Client Initializer Metaclass;
#     Initializes MacOSX & Windows instant_client for local testing.
#     client installation for MacOSX: https://confluence.gfk.com/pages/viewpage.action?pageId=345064535
#     """
#     __initialized__: bool = False
#
#     def __call__(cls, *args, **kwargs):
#         cls.__exec_config__ = InstantClientCfg()
#         cls.__exec_logger__ = logging.getLogger('Oracle')
#         cls.__exec_logger__.info('Oracle Client initializes.')
#
#         if not cls.__initialized__:
#             try:
#                 if sys.platform.startswith("darwin"):
#                     lib_dir = cls.__exec_config__.mac_client
#                     cx_Oracle.init_oracle_client(lib_dir=lib_dir)
#                 elif sys.platform.startswith("win32"):
#                     lib_dir = cls.__exec_config__.win_client
#                     cx_Oracle.init_oracle_client(lib_dir=lib_dir)
#                 cls.__initialized__ = True
#             except Exception as err:
#                 cls.__exec_logger__.error('Oracle Client failed to initialize.')
#                 cls.__exec_logger__.error(err)
#         return super(ClientInitializer, cls).__call__(*args, **kwargs)