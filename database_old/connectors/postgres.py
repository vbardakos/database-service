from pydantic import StrictStr, Field, StrictInt
from database.domain.connection_old import Connection
from typing import Any, Annotated


class PGConnection(Connection):
    dbname: Annotated[StrictStr, Field(alias='database')]
    host: StrictStr
    user: StrictStr
    port: StrictInt = 5432

    def _connection(self, conn: 'PGConnection') -> str:
        info = conn.dict(exclude={'name'}) | {'password': self.password.get_secret_value()}
        return ' '.join(f'{k}={v}' for k, v in info.items())
