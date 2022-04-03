import inspect
from functools import wraps
from logging import getLogger
from sys import argv
from pathlib import Path


def log(func):
    logger_name = 'app.server' if 'server.py' in argv[0] else 'app.client'
    logger = getLogger(logger_name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1]
        caller_file = Path(caller.filename)
        logger.debug(f'{caller_file.name}:{caller.lineno} {caller.function}() -> {func.__module__}.{func.__name__}({args=}, {kwargs=})')

        func_result = func(*args, **kwargs)
        return func_result

    return wrapper
