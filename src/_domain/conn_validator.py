from enum import Enum
from cerberus import Validator
from dataclasses import is_dataclass, asdict, dataclass
from typing import Tuple, NewType


class ConnValidator(Validator):
    def __init__(self, schema, purge_unknown: bool = True):
        super(ConnValidator, self).__init__(schema, purge_unknown=purge_unknown)

    def validate(self, document: dict) -> dict:
        return super(ConnValidator, self).validate(self._get_dataclass(document))

    def normalized(self, document: dict) -> dict:
        return super(ConnValidator, self).normalized(self._get_dataclass(document))

    def normalized_with_remainder(self, document: dict) -> Tuple[dict, dict]:
        normalize = self.normalized(document)
        remainder = {k: document[k] for k in document.keys() - normalize.keys()}
        return normalize, remainder

    @staticmethod
    def _get_dataclass(obj):
        return asdict(obj) if is_dataclass(obj) else obj

    @staticmethod
    def _normalize_coerce_enum(item):
        return item.value if isinstance(item, Enum) else item


Dataclass = NewType('Dataclass', is_dataclass)

if __name__ == '__main__':
    @dataclass
    class A:
        x: int = 1

    def foo(x: Dataclass):
        return x

    print(foo(A()))

