from pydantic import SecretStr, Field, validator
from typing import Annotated, Any

from service.domain.settings._active import ActiveEnvironment
from service.domain.settings._secret import GoogleSecret
from service.domain.settings._extras import ExtraSettings


class BaseConnectionSettings(ActiveEnvironment):
    # fixme : type
    user: Annotated[str, Field(min_length=4)]
    type: Any | None
    password: SecretStr | None
    port: Annotated[int | None, Field(ge=1000, le=99999)]
    host: Annotated[str, Field(min_length=4)]
    database: Annotated[str, Field(min_length=4)]
    google: GoogleSecret = GoogleSecret(project=None, secret=None)
    extras: ExtraSettings = ExtraSettings(instant_client=None)

    class Config:
        allow_mutation = True
        env_nested_delimiter = '__'

    @validator('google', always=True)
    def check_password(cls, secret: GoogleSecret, values: dict):
        if secret.is_empty is (values.get('password') is None):
            return secret
        else:
            # fixme : raise Pydantic Error
            raise ValueError('Accepts either password or a google secret')

    def retrieve_password(self):
        if self.password is None:
            self.password = SecretStr(self.google.retrieve_password())


if __name__ == '__main__':
    print(BaseConnectionSettings())