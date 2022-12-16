from enum import Enum
from pydantic import PyObject
from pydantic.fields import ModelField


class Environment(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


class SchemaPyObject(PyObject):
    @classmethod
    def __modify_schema__(cls, field_schema, field: ModelField | None):
        if field:
            field_schema['type'] = 'string'
            field_schema['special_type'] = field.type_.__name__
