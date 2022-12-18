from pathlib import Path
from pydantic import BaseModel, Extra, Field
from typing import Annotated

from service.domain.types import SchemaPyObject, FlexDirectoryPath


class ExtraSettings(BaseModel):
    # fixme : relative dir from env_file
    logging_object: Annotated[SchemaPyObject, Field(exclude=False)] = 'logging.getLogger'
    instant_client: FlexDirectoryPath | None
    reading_directory: FlexDirectoryPath = Path()
    writing_directory: FlexDirectoryPath = Path()
    connection_kwargs: dict = Field(default_factory=dict)
    cursor_kwargs: dict = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        extra = Extra.allow
