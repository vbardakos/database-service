import google_crc32c
from google.cloud import secretmanager
from pydantic import BaseModel, validator


class GSecret(BaseModel):
    project: str | None = None
    secret: str | None = None
    version: str = 'latest'

    @validator('secret', always=True)
    def check_population(cls, v, values):
        if isinstance(v, str) ^ isinstance(values['project'], str):
            raise ValueError('Either both project & database should be set or None')
        return v

    def retrieve_password(self):
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": self._secret_name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response
        else:
            return response.payload.data.decode("UTF-8")

    @property
    def _secret_name(self):
        return f"projects/{self.project}/secrets/{self.secret}/versions/{self.version}"

    @property
    def is_empty(self) -> bool:
        return self.project is None
