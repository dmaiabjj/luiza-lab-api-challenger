import enum


class ErrorCode(enum.Enum):
    ENTITY_NOT_FOUND = 1


class BaseError(dict):
    def __init__(self, code, message):
        dict.__init__(self, code=code, message=message)


class BaseCustomError(dict):
    def __init__(self, code, message):
        dict.__init__(self, error=BaseError(code=code, message=message))
