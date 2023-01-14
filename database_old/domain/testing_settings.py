from pydantic import *
from pydantic.env_settings import BaseConfig
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Type, Any, ClassVar
from dotenv import find_dotenv


DnsType = TypeVar('DnsType')


class EnvConfig(BaseSettings.Config):
    env_file = find_dotenv()


class EnvConnect(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    database: str

    class Config(EnvConfig):
        ...


def get_connection_from_env(common_prefix: str | None = None, **field_aliases):
    EnvConnect.Config.env_prefix = common_prefix or ''
    EnvConnect.Config.fields = {k: {'env': v} for k, v in field_aliases.items()}
    return create_model('_EnvConn', __base__=EnvConnect)


class A(BaseModel):
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x


class B(BaseModel):
    __root__: list[A] = Field(default_factory=list, unique_items=True)

    class Config:
        validate_assignment = True

    @validate_arguments
    def add(self, alpha: A):
        self.__root__ += [alpha]


if __name__ == '__main__':
    # EnvConnect.add_common_prefix('pg_')
    # EnvConnect.Config.env_prefix = 'pg_'
    # print(EnvConnect.__config__)
    # EnvConfig.env_prefix = 'pg_'
    # print(EnvConnect.__config__)
    # print({k: getattr(EnvConnect.Config, k) for k in dir(EnvConnect.Config)})
    # conn1 = get_connection_from_env('pg_', user='user')
    # conn2 = get_connection_from_env('pg_')
    # print(conn1(), conn2())
    # B.parse_obj([A(x=1, y=2), A(x=2, y=4)])
    b = B()
    b.add(A(x=1, y=2))
    b.add(A(x=1, y=3))
    print(b)


    # dns = PostgresDsn('postgres://flyway:mysecretpassword@localhost/newron', scheme='postgres')

