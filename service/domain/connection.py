from pydantic import Field, validate_arguments, create_model, DirectoryPath, PyObject
from pydantic.generics import GenericModel
from typing import TypeVar, Generic
from enum import Enum

from service.domain.settings import BaseConnectionSettings, ExtraSettings, GoogleSecret, ActiveEnvironment
from service.domain.utilities import jsonify, pyobject_string


NameT = TypeVar('NameT', bound=str | Enum)


class ConnectionFactory(GenericModel, Generic[NameT]):
    name: NameT
    conn: BaseConnectionSettings | None = None
    conn_kwargs: dict = Field(default_factory=dict)
    initialized: bool = False
    _env_directory: DirectoryPath | None = None
    adapter: PyObject | None

    class Config:
        json_dumps = jsonify(pyobject_string)
        use_enum_values = True

    @validate_arguments
    def __init__(self,
                 *,
                 name: NameT,
                 user: str | None = None,
                 password: str | None = None,
                 host: str | None = None,
                 port: int | None = None,
                 database: str | None = None,
                 google: GoogleSecret | None = None,
                 extras: ExtraSettings | None = None
                 ):
        super(ConnectionFactory, self).__init__(name=name)
        self.conn_kwargs = dict(user=user, password=password, host=host, port=port,
                                database=database, google=google, extras=extras)
        self.conn_kwargs = {k: v for k, v in self.conn_kwargs.items() if v is not None}

    def initialize(self, reinitialize_outdated: bool = True):
        if not self.initialized or reinitialize_outdated and self.conn.instance_is_outdated:
            new_connection = self._build_settings()
            new_connection.retrieve_password()
            self.conn = new_connection
            self.adapter = new_connection.type(new_connection)
            self.initialized = True

    def _build_settings(self):
        BaseConnectionSettings.Config.env_prefix = '_'.join((ActiveEnvironment().current_environment, self.name, ''))
        return create_model(f'ConnectionSettings', __base__=BaseConnectionSettings)(**self.conn_kwargs)

    def select(self, *columns: str, table: str, limit: int | None = None, order_by: str | None = None):
        ...

    def __eq__(self, other):
        return self.name == other.name


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from time import time
    import timeit

    conn1 = ConnectionFactory(name='pg')
    conn1.initialize()
    stmt = """
    select *
    from pg_class
    union all
    select *
    from pg_class
    union all
    select *
    from pg_class
    union all
    select *
    from pg_class
    union all
    select *
    from pg_class
    """
    stmt = "select distinct on (data_type) * from information_schema.columns where table_schema = 'sales'"
    head = [(x[0], object) for x in conn1.adapter._desc(stmt)]
    rows = conn1.adapter._execute(stmt=stmt, fetch=0, fetchall=True, commit=False, row_factory=lambda x: x)

    print(conn1)

    # print(np.fromiter(rows, dtype=head)[1])
    # print(head)

    code = '''
stmt = """
select *
from pg_class
union all
select *
from pg_class
union all
select *
from pg_class
union all
select *
from pg_class
union all
select *
from pg_class
"""

def fetcher(stmt):
    with psycopg.connect('postgres://flyway:mysecretpassword@localhost:5432/newron') as conn:
        with conn.cursor() as cursor:
            cursor.execute(stmt)
            # yield [(c[0], object) for c in cursor.description]
            for row in cursor:
                yield row

rows = fetcher(stmt)

np.asarray(tuple(rows), dtype=object)
# tuple(rows)
# np.fromiter(rows, dtype=np.dtype((object, len(next(rows)))))
# new = np.fromiter(rows, dtype=next(rows))
'''
    # np.fromiter(rows, dtype=np.dtype((object, len(next(rows)))))

    # np.asarray(tuple(fetcher(stmt)), dtype=object)

    # np.asarray(tuple(rows), dtype=object)
    #
    # print(timeit.repeat(code, setup='import numpy as np; import psycopg', number=5, repeat=10))

    # conn.select('period', 'country', 'item', from='sales.item')


    # start = time()
    # for _ in range(1):
    #     list_rows = list(rows)
    # print(round(time() - start, 5))
    #
    # print('total rows', len(list_rows))

    # arr = np.empty(shape=(0, len(head)), dtype=object)
    # for row in rows:
    #     arr = np.append(arr, [row], axis=0)
    # print(np.fromiter(rows, dtype=np.dtype((object, len(head)))))



    # start = time()
    # for _ in range(n):
    #     np.asarray(list_rows, dtype=object)
    # print(round(time() - start, 5))

    # start = time()
    # for _ in range(n):
    #     pd.DataFrame(data=list_rows, columns=head)
    # print(round(time() - start, 5))

