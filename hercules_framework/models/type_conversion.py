"""Type conversions generated from quicktype.com
"""
from datetime import datetime
from typing import Any, Callable, List, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")


def from_int(x: Any) -> int:

    return int(float(x)) if x else int(0)


def from_float(x: Any) -> float:

    return float(x)


def to_float(x: Any) -> float:

    return float(x) if x is not None else float(0)


def from_str(x: Any) -> str:
    if str(x) in ["None", "none"]:
        return None

    return str(x)


def from_bool(x: Any) -> bool:

    return bool(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:

    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:

    return cast(Any, x).to_dict()


def from_stringified_bool(x: str) -> bool:
    if type(x) == bool:
        return x
    if x in ["true", "True"]:
        return True
    if x in ["false", "False"] or not x:
        return False
    raise Exception("String {} not converted".format(x))
