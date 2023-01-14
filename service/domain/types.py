from enum import Enum
from pydantic import PyObject, DirectoryPath, PathNotADirectoryError, PathNotExistsError, PathError
from pydantic.errors import _PathValueError
from pydantic.fields import ModelField
from pathlib import Path


class Environment(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


class IllegalRelativeDirectory(PathError):
    pass


class SchemaPyObject(PyObject):
    @classmethod
    def __modify_schema__(cls, field_schema, field: ModelField | None):
        if field:
            field_schema['type'] = 'string'
            field_schema['description'] = field.type_.__name__


class FlexDirectoryPath(DirectoryPath):
    _flavour = Path()._flavour

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, directory: str):
        path = Path(directory).resolve()
        if path.is_dir():
            return cls(path)
        elif '...' in str(path):
            raise IllegalRelativeDirectory(msg="Replace '...' with '../..'", path=path)
        elif path.exists():
            raise PathNotADirectoryError(path=path)
        else:
            raise PathNotExistsError(path=path)

    @classmethod
    def validated_join(cls, init: Path, *joins: str):
        if joins:
            join, *joins = joins
            return cls.validated_join(cls.validate(init / join), *joins)
        else:
            return init


if __name__ == '__main__':
    from pathlib import Path
    from pydantic import BaseModel

    class A(BaseModel):
        x: FlexDirectoryPath

    path = Path('../../service')
    a = A(x=path)
    print(FlexDirectoryPath.validated_join(a.x, 'domain', 'adapters'))
