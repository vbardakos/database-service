from pathlib import Path
from pydantic import BaseModel, Extra, DirectoryPath, Field, PyObject
from typing import Annotated


class ExtraSettings(BaseModel):
    logger: Annotated[PyObject, Field(exclude=True)] = 'logging.getLogger'
    instant_client: DirectoryPath | None
    reading_directory: DirectoryPath = Path()
    writing_directory: DirectoryPath = Path()
    connection_kwargs: dict = Field(default_factory=dict)
    cursor_kwargs: dict = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        extra = Extra.allow
