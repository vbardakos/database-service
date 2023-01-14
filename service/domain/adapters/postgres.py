import psycopg
from pydantic import PostgresDsn, SecretStr
from typing import Callable

from service.domain.settings import BaseConnectionSettings
from service.domain.adapters.adapter import BaseAdapter


class PGAdapter(BaseAdapter):
    _scheme: str = 'postgres'

    def _get_dsn(self, conn: BaseConnectionSettings):
        return PostgresDsn.build(scheme=self._scheme,
                                 user=conn.user,
                                 password=conn.password.get_secret_value(),
                                 host=conn.host,
                                 port=str(conn.port) if conn.port else conn.port,
                                 path=f'/{conn.database}')

    def _execute(self, stmt: str, fetch: int, fetchall: bool, commit: bool, row_factory: Callable):
        self._log.info('starts')
        with psycopg.connect(self._dsn, **self._arg.connection_kwargs) as conn:
            with conn.cursor(**self._arg.cursor_kwargs) as cursor:
                cursor.execute(stmt)
                if fetch:
                    for row in cursor.fetchmany(fetch):
                        yield row_factory(row)
                elif fetchall:
                    for row in cursor.fetchall():
                        yield row_factory(row)
                yield [x[0] for x in cursor.description]
            if commit:
                conn.commit()
        self._log.info('finished')

    def _desc(self, stmt: str):
        with psycopg.connect(self._dsn, **self._arg.connection_kwargs) as conn:
            with conn.cursor(**self._arg.cursor_kwargs) as cursor:
                cursor.execute(stmt)
                return cursor.description

if __name__ == '__main__':
    PROD_PG_USER = 'flyway'
    PROD_PG_HOST = 'production'
    PROD_PG_PORT = 5432
    PROD_PG_DATABASE = 'newron'
    PROD_PG_PASSWORD = SecretStr('mysecretpassword')

    # print(PostgresDsn(f'postgres://user:pass@host.com:5432/newron', scheme='postgres'))
    # pg = PostgresDsn.build(
    #     scheme='postgres',
    #     user=PROD_PG_USER,
    #     password=PROD_PG_PASSWORD.get_secret_value(),
    #     host=PROD_PG_HOST,
    #     port=str(PROD_PG_PORT),
    #     path='/' + PROD_PG_DATABASE,
    # )
    # print('pg', PostgresDsn(pg, scheme='postgres').path)