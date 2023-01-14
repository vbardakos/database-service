import os
from pydantic import BaseSettings, Field, validator, validate_arguments, StrictStr
from typing import Annotated, ClassVar

from service.domain.types import Environment
from service.domain.utilities import dotenv_directory


class ActiveEnvironment(BaseSettings):
    environment_varname: ClassVar[StrictStr] = 'override_environment'
    default_environment: Annotated[Environment | None, Field(env='active_environment')]
    current_environment: Annotated[Environment | None, Field(env='override_environment')]

    class Config:
        env_file = dotenv_directory()
        allow_mutation = False
        use_enum_values = True

    @validator('current_environment', always=True)
    def check_default_environment(cls, environment: Environment | None, values: dict):
        return environment or values.get('default_environment')

    @classmethod
    @validate_arguments(config=dict(use_enum_values=True))
    def set_current_environment(cls, env: Environment):
        os.environ[cls.environment_varname] = env

    @classmethod
    def remove_current_environment(cls):
        os.environ.pop(cls.environment_varname, None)

    @property
    def instance_is_outdated(self):
        return self.current_environment != ActiveEnvironment().current_environment
