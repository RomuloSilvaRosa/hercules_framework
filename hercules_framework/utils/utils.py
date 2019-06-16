import datetime
import inspect
import logging
import os
import sys
from typing import List
from uuid import UUID, uuid4
from hercules_framework.settings import DEBUG_MODE


def fake_object(obj, **kwargs):
    par = get_mock_parameters(obj, **kwargs)
    return obj(**par)


def get_mock_parameters(function, **kwargs):
    args = inspect.getfullargspec(function).args
    try:
        args.remove('self')
    except:
        pass
    sig = inspect.signature(function)
    for item in args:
        if item not in kwargs.keys():
            post_process = None
            typ = sig.parameters.get(item).annotation
            if typ is inspect._empty:
                typ = None
            elif typ is datetime.datetime:
                typ = datetime.datetime.now
            elif typ is UUID:
                typ = uuid4
                post_process = str
            try:
                try:
                    kwargs[item] = typ()
                except:
                    kwargs[item] = get_mock_parameters(typ)
            except:
                kwargs[item] = None
            if post_process:
                kwargs[item] = post_process(kwargs[item])
    return kwargs


DEV_NULL = open(os.devnull, 'w+')


def supress_log(f):

    def wrapper(*args, **kwargs):
        if not(DEBUG_MODE):
            disable_logs()
            sys.stdout = DEV_NULL
            sys.stderr = DEV_NULL
        return f(*args, **kwargs)

    return wrapper


def disable_logs(log_names: List[str] = []) -> None:
    filtered_logs = []
    log_keys = logging.Logger.manager.loggerDict.keys()
    if len(log_names) == 0:
        filtered_logs = log_keys
    else:
        for log in log_names:
            for key in log_keys:
                if key.startswith(log):
                    filtered_logs.append(key)
    for filter_key in filtered_logs:
        log = logging.getLogger(filter_key)
        log.disabled = True
        log.addHandler(logging.NullHandler())
        log.propagate = False
        log.addFilter(lambda record: False)


class SimpleMock:
    ret = None

    def __init__(self, ret=None):
        self.ret = ret

    def __call__(self, *args, **kwargs):
        return self.ret
