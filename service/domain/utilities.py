import json
from dotenv import find_dotenv
from functools import lru_cache
from typing import Callable
from types import ModuleType


def json_dumper(obj: dict, **kwargs):

    def jsonify_pyobj(key, value):
        if isinstance(value, ModuleType):
            value = value.__module__
        elif isinstance(value, Callable):
            value = f'{value.__module__}.{value.__name__}'.replace('__main__.', '')
        return key, value

    return json.dumps(dict(map(jsonify_pyobj, obj.keys(), obj.values())), **kwargs)


@lru_cache(maxsize=1)
def dotenv_directory():
    return find_dotenv()
