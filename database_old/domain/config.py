from pydantic import BaseSettings, ConstrainedStr, SecretStr, ConstrainedInt, Field, validator
from typing import Annotated
from dotenv import find_dotenv
from enum import Enum
from functools import lru_cache

from database.domain.gsecret import GSecret


class Environment(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


class ActiveEnv(BaseSettings):
    active_environment: Annotated[Environment | None, Field(env='active_env')]
    current_environment: Annotated[Environment | None, Field(env='override_env')]

    class Config:
        env_nested_delimiter = '_'
        env_file = find_dotenv()
        use_enum_values = True

    @validator('current_environment', always=True)
    def check_current_environment(cls, v, values):
        return v if v is not None else values.get('active_environment')


@lru_cache(maxsize=1)
def get_environment():
    return ActiveEnv()


class DatabaseSettings(ActiveEnv):
    user: ConstrainedStr
    host: ConstrainedStr
    port: ConstrainedInt
    database: ConstrainedStr
    google: GSecret = GSecret()
    password: SecretStr | None

    @validator('password', always=True)
    def check_password(cls, password, values):
        google: GSecret = values['google']
        if isinstance(password, SecretStr) ^ google.is_empty:
            raise ValueError('Accepts either a password or a google secret, not both.')
        elif password is not None:
            return password
        else:
            return SecretStr(google.retrieve_password())

    @property
    def is_outdated(self):
        return self.current_environment != ActiveEnv().current_environment
