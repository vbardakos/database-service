from pydantic import BaseModel, Field, PositiveInt, constr, validate_arguments
from typing import Literal


VID = PositiveInt | None
MD5 = constr(strict=True, min_length=32, max_length=32)


class SchemaParser(BaseModel):
    name: Literal['sales', 'stage']
    locked: MD5 = Field(default='')
    versioned: dict[VID, MD5] = Field(default_factory=dict)
    repeating: dict[VID, MD5] = Field(default_factory=dict)

    @validate_arguments
    def add(self, is_version: bool, vid: VID, vhash: MD5):
        match is_version, vid:
            case True, None:
                self.locked = vhash
            case True, _:
                self.versioned[vid] = vhash
            case _:
                self.repeating[vid] = vhash


class MetaParser(BaseModel):
    version: PositiveInt = Field(default=1)
    schemas: list[SchemaParser] = Field(default_factory=list)

    def add_schema(self, name: str):
        self.schemas.append(SchemaParser(name=name))

    def add_record(self, record: tuple):
        self.schemas[-1].add(*record)

    def bump_version(self):
        self.version += 1
