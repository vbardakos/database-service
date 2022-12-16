from pathlib import Path
from pydantic import BaseModel, Extra, DirectoryPath, Field
from typing import Annotated

from service.domain.types import SchemaPyObject


class ExtraSettings(BaseModel):
    logging_object: Annotated[SchemaPyObject, Field(exclude=False)] = 'logging.getLogger'
    instant_client: DirectoryPath | None
    reading_directory: DirectoryPath = Path()
    writing_directory: DirectoryPath = Path()
    connection_kwargs: dict = Field(default_factory=dict)
    cursor_kwargs: dict = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        extra = Extra.allow
