from pydantic import StrictStr, validator
from pydantic.generics import GenericModel, Generic
from encodings import utf_8
from typing import TypeVar


Prj_T = TypeVar('Prj_T', bound=StrictStr)
Scr_T = TypeVar('Scr_T', bound=StrictStr)
UTF_8 = utf_8.getregentry().name


class GoogleSecret(GenericModel, Generic[Prj_T, Scr_T]):
    project: Prj_T | None
    secret: Scr_T | None
    version: StrictStr = 'latest'

    class Config:
        allow_mutation = False
        use_enum_values = True

    @validator('secret', always=True)
    def check_secret(cls, secret, values):
        if bool(secret) is bool(values.get('project')):
            return secret
        else:
            # fixme : change to pydantic error
            raise ValueError('Either both project & secret should be set or None')

    def retrieve_password(self):
        import google_crc32c
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": self._secret_name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            # fixme : Add pydantic error
            raise ValueError('Data corruption detected.')
        else:
            return response.payload.data.decode(UTF_8)

    @property
    def _secret_name(self):
        return f'projects/{self.project}/secrets/{self.secret}/versions/{self.version}'

    @property
    def is_empty(self) -> bool:
        return bool(self.project)
