import json
from dotenv import find_dotenv
from functools import lru_cache
from typing import Callable, Any, Generator


def dict_deep_mapper(obj: dict, mapper: Callable[[Any], Any]) -> Generator:
    for k, v in obj.items():
        if isinstance(v, dict):
            yield k, dict(dict_deep_mapper(v, mapper))
        else:
            yield k, mapper(v)


def pyobject_string(obj: Any):
    if hasattr(obj, '__name__'):
        return '.'.join([obj.__module__, obj.__name__]).replace('__main__.', '')
    elif hasattr(obj, '__call__'):
        return '.'.join([obj.__module__, type(obj).__name__]).replace('__main__.', '')
    else:
        return obj


def get_logger(name: str):
    import logging
    logger = logging.getLogger(name)
    logger.setLevel('DEBUG')
    logger.addHandler(logging.StreamHandler())
    return logger


def jsonify(*mappers: Callable[[Any], Any]):
    def jsonify_mapper(obj, **kwargs):
        for mapper in mappers:
            obj = dict_deep_mapper(dict(obj), mapper)
        else:
            return json.dumps(dict(obj), **kwargs)

    return jsonify_mapper


@lru_cache(maxsize=1)
def dotenv_directory():
    return find_dotenv()
