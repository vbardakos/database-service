from enum import Enum


class Environment(str, Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'
