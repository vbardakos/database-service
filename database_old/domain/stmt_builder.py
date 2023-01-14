import sqlparse
from pydantic import BaseModel, ConstrainedStr, Field
from typing import Annotated, Any


class MetaColumn(BaseModel):
    name: ConstrainedStr
    description: ConstrainedStr
    type: type
    type_constraint: Any
    primary: bool
    nullable: bool


class MetaTable(BaseModel):
    ...


class StmtBuilder(BaseModel):
    ...
