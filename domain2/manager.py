import asyncio
import psycopg
from pathlib import Path
from domain2.connect import PostgresCfg
from domain2.parsers import MetaParser, SchemaParser


class MetadataManager:
    file = Path(__file__).parent.joinpath('.schema.json')
    flyway_sql = Path(__file__).parent.joinpath('generate.sql')
    schemas: set[str] = set(SchemaParser.schema()['properties']['name']['enum'])

    def __init__(self, connection: str, metadata_path: Path = file):
        self._conn = connection
        self._meta = MetaParser()
        self._path = metadata_path

    def retrieve_metadata(self) -> MetaParser:
        if self._path.is_file():
            self._meta = MetaParser.parse_raw(self._path.open().read())
        else:
            raise FileNotFoundError('metadata schema is not found. Generate a new schema')

    async def _generate_metadata(self, flyway: str, schema: str, version: int):
        async with await psycopg.AsyncConnection.connect(self._conn) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(flyway % dict(_schema=schema, lock=version))
                return await cursor.fetchall()

    async def _populate_metadata(self, flyway, **version_locks: int):
        for schema, version in version_locks.items():
            self._meta.add_schema(schema)
            metadata = await self._generate_metadata(flyway, schema, version)
            for record in metadata:
                self._meta.add_record(record)

    def generate(self, **version_locks: int):
        if self.schemas == version_locks.keys():
            stmt = self.flyway_sql.open().read()
            async_loop = asyncio.new_event_loop()
            try:
                async_loop.run_until_complete(self._populate_metadata(stmt, **version_locks))
                self._path.open('w').write(self._meta.json(indent=4))
            finally:
                async_loop.run_until_complete(
                    async_loop.shutdown_asyncgens()
                )
                async_loop.close()

    def evaluate_schema(self):
        meta = self._meta.copy() if self._meta else self.retrieve_metadata().copy()
        self.generate(**{p.name: min(p.versioned.keys()) - 1 for p in meta.schemas})
        if meta != self._meta:
            pass
        elif all(p1.locked == p2.locked for p1, p2 in zip(meta.schemas, self._meta.schemas)):
            self._meta.bump_version()
            print(True)


# if __name__ == '__main__':
#     manager = MetadataManager(PostgresCfg.get_connection_string())
#     manager.retrieve_metadata()
    # manager.generate(sales=159, stage=40)
    # manager.evaluate_schema()