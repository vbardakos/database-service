import os
from pydantic import BaseModel, validator, ConstrainedStr, validate_arguments, create_model, PyObject
from database.domain.config import DatabaseSettings, ActiveEnv, Environment, GSecret, get_environment
from enum import Enum


class Connection(BaseModel):
    name: ConstrainedStr | Enum
    dns_type: PyObject = 'pydantic.PostgresDsn'
    connection: DatabaseSettings = None

    class Config:
        use_enum_values = True

    def __init__(self,
                 name: str | Enum,
                 user: str | None = None,
                 password: str | None = None,
                 host: str | None = None,
                 port: int | None = None,
                 database: str | None = None):
        conn_info = dict(user=user, password=password, host=host, port=port, database=database)
        conn_info = {k: v for k, v in conn_info.items() if v is not None}
        conn_info |= dict(google=GSecret()) if conn_info.get('password') else dict()
        super(Connection, self).__init__(name=name, connection=self._create_connection(name, conn_info))

    def initialize(self, skip_initialized: bool = True, skip_outdated: bool = False):
        if not skip_initialized or self.connection is None or (not skip_outdated and self.connection.is_outdated):
            ...
        else:
            ...

        # skip_initialized and self.connection is not None
        # not skip_initialized or self.connection is None


    def _create_connection(self, name: str, conn_kwargs: dict):
        DatabaseSettings.__config__.env_prefix = '_'.join([ActiveEnv().current_environment, name, ''])
        return create_model(f'{name.upper()}Settings', __base__=DatabaseSettings)(**conn_kwargs)

    # @validator('connection', always=True)
    # def check_connection(cls, _, values):
    #     name = values['name']
    #     DatabaseSettings.__config__.env_prefix = '_'.join([ActiveEnv().current_environment, name]) + '_'
    #     return create_model(f'{name.upper()}Settings', __base__=DatabaseSettings)()

    @classmethod
    @validate_arguments
    def override_environment(cls, name: Environment):
        os.environ['override_env'] = name

    @classmethod
    def remove_override(cls):
        os.environ.pop('override_env')


if __name__ == '__main__':
    conn = Connection('PG')
    conn2 = Connection('PG')
    print(conn.connection.is_outdated, conn2.connection.is_outdated)
    conn.override_environment('test')
    print(conn.connection.is_outdated, conn2.connection.is_outdated)
    conn.remove_override()
    print(conn.connection.is_outdated, conn2.connection.is_outdated)


