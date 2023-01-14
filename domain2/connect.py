import json
import asyncio
from pathlib import Path
from dataclasses import dataclass, fields
from pydantic import *
from typing import Type, Literal

import psycopg
from environs import Env

DEFAULT_POOL_SIZE: int = 8

env = Env()
env.read_env()
envclass = dataclass(init=False, frozen=True, repr=False, eq=False)


@envclass
class ConnectionCfg:
    dbname: str
    host: str
    port: int
    user: str
    password: str

    @classmethod
    def get_connection_string(cls: Type[envclass], sep=" ") -> str:
        fmt_fields = [f"{f.name}={f.default}" for f in fields(cls)]
        return sep.join(fmt_fields)


@envclass
class PostgresCfg(ConnectionCfg):
    dbname: str = env.str('PG_DATABASE', 'newron')
    host: str = env.str('PG_HOST', 'localhost')
    port: int = env.int('PG_PORT', 5432)
    user: str = env.str('PG_USER', 'postgres')
    password: str = env.str('PGPASSWORD', 'ecosystem')
