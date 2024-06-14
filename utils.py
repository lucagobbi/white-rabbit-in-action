import inspect
import re
from typing import Callable


def extract_args_as_kwargs(func: Callable, *args, **kwargs) -> dict:
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())

    for name, arg in zip(param_names, args):
        if name not in kwargs:
            kwargs[name] = arg
    return kwargs


def parse_cron_expression(cron_expression: str):
    keys = ['minute', 'hour', 'day', 'month', 'day_of_week']
    return dict(zip(keys, cron_expression.split()))


def extract_int_from_string(s: str):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    raise ValueError("No integer found in the string.")
