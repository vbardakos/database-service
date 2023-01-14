from pydantic import BaseSettings, create_model, ConstrainedStr, SecretStr, ConstrainedInt, Field, BaseModel, validator
from typing import Literal, Type, ClassVar
from dotenv import find_dotenv
from enum import Enum
import google_crc32c
from google.cloud import secretmanager


class Environment(Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


class Database(Enum):
    POSTGRES = 'pg'
    ORACLE = 'ora'


class ActiveEnv(BaseSettings):
    active_env: Literal['prod', 'dev', 'test', None] = Field(None, env='active_env')

    class Config:
        env_nested_delimiter = '_'
        env_file = find_dotenv()


class GlobalDbSettings(ActiveEnv):
    user: ConstrainedStr
    host: ConstrainedStr
    port: ConstrainedInt
    database: ConstrainedStr
    google: GSecret = Field(GSecret(), exclude=True)
    password: SecretStr | None = None

    @validator('password', always=True)
    def check_password(cls, v, values):
        google: GSecret = values['google']
        if isinstance(v, SecretStr) ^ google.is_empty:
            raise ValueError('Set either a password or google secret.')
        elif v is not None:
            return v
        else:
            return SecretStr(google.retrieve_password())


class ProdSettings(GlobalDbSettings):
    class Config(GlobalDbSettings.Config):
        env_prefix = Environment.PROD.value + '_'


class DevSettings(GlobalDbSettings):
    class Config(GlobalDbSettings.Config):
        env_prefix = Environment.DEV.value + '_'


class TestSettings(GlobalDbSettings):
    class Config(GlobalDbSettings.Config):
        env_prefix = Environment.TEST.value + '_'


class Connection(BaseModel):
    name: ConstrainedStr | Enum
    connection: GlobalDbSettings | None = None
    _env: ClassVar[Literal['prod', 'dev', 'test', None]] = ActiveEnv().active_env

    class Config:
        use_enum_values = True

    @validator('connection', always=True)
    def check_connection(cls, v, values):
        conn = values['name']
        match cls._env:
            case 'prod':
                return cls._get_connection(conn, base_model=ProdSettings)
            case 'dev':
                return cls._get_connection(conn, base_model=DevSettings)
            case 'test':
                return cls._get_connection(conn, base_model=TestSettings)

    @classmethod
    def enforce_environment(cls, name: Literal['prod', 'dev', 'test', None]):
        cls._env = name or ActiveEnv().active_env

    @staticmethod
    def _get_connection(connection_name: str, base_model: Type[GlobalDbSettings]):
        base_model.__config__.env_prefix += connection_name + '_'
        return create_model(f'{connection_name.capitalize()}Settings', __base__=base_model)()


if __name__ == '__main__':
    # settings = Settings(common_prefix=Database.POSTGRES)
    # print(settings.get_settings()().dict())
    # Settings.enforce_environment('test')
    # print(settings.get_settings()(user='hello'))
    conn1 = Connection(name='PG')
    Connection.enforce_environment('test')
    conn2 = Connection(name='PG')
    print(conn1, conn2.dict(), sep='\n\n')

