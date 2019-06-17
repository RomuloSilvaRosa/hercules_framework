""" global settings. """
import types
from typing import List

from decouple import Undefined
from decouple import config as _config


def get_all(local_vars: dict) -> List[str]:
    """Get all public class/function/var
    """

    _all = []
    for item in local_vars.copy().keys():
        if not str(item).startswith('_') and not item in dir(types):
            _all.append(str(item))
    return _all


def config(config_name, default=None, cast=None, private=False):

    if cast is None and default is not None:
        cast = type(default)
    cfg = None

    try:
        cfg = _config(config_name, default=default or Undefined(),
                      cast=cast or Undefined())
    except Exception:
        cfg = cast(default) if cast else default
    if not private:
        print(config_name + ' = ' + str(cfg))
    return cfg


DEBUG_MODE = config('DEBUG', default=False)
OUT_FOLDER = config('OUT_FOLDER', default='out/')
FIREHOSE_ROLE = config('FIREHOSE_ROLE')
ENABLE_STREAM = config('ENABLE_STREAM', default=False)
KINESIS_FIREHOSE_STREAM_DATA_NAME = config('KINESIS_FIREHOSE_STREAM_DATA_NAME',
                                           default='kinesis-firehose-hml',
                                           private=True)
AWS_REGION = config('AWS_REGION')

CACHE_PORT = config('CACHE_PORT', default=6379)
CACHE_HOST = config('CACHE_HOST', default='localhost')
CACHE_DB = config('CACHE_DB', default='0')

APP_FOLDER = config('APP_FOLDER', cast=str)
ENVIRONMENT = config('ENVIRONMENT', default='dev')
HERCULES_BASE_PATH = '/hercules'
APP_NAME = config
AUTH_CRYPT_KEY = config(
    'AUTH_CRYPT_KEY', default='60c4c83b426005a3e81278696b6d7b248c2b08c93033af60d525746a1e972e0a', private=True)
SERVICE_NAME = APP_FOLDER.replace('_', '-')

CRUD_SELLER_HOST = config('CRUD_SELLER_HOST', default='http://localhost:4422')
CRUD_CLIENT_HOST = config('CRUD_CLIENT_HOST', default='http://localhost:4423')
CRUD_ORDER_HOST = config('CRUD_ORDER_HOST', default='http://localhost:4424')


class RecordType:
    priority = 'priority'


__all__ = get_all(locals())
