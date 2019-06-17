from datetime import datetime
from typing import Any, Callable, List, Type, TypeVar, cast
import dateutil.parser
from stringcase import camelcase, snakecase

from hercules_framework.settings import get_all
from hercules_framework.utils.type import check_type


class BaseModel:
    """The std models use the json convention name
    format https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format
    """

    def to_dict(self):
        response = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                aux = BaseModel()
                aux.__dict__.update(value)
                value = aux.to_dict()
            response[camelcase(key.replace('-', '_').lower())] = value
        return response

    @classmethod
    def from_dict(cls, dict_obj: dict) -> 'Base':
        check_type(dict, dict_obj=dict_obj)

        input_dict = dict()
        for key, value in dict_obj.items():
            input_dict[snakecase(key)] = value
        aux = cls()
        aux.__dict__.update(input_dict)
        return aux


# Type conversions generated from quicktype.com


T = TypeVar("T")


def from_int(x: Any) -> int:
    return int(float(x)) if x else 0


def from_float(x: Any) -> float:
    return float(x) if x else float(0)


def to_float(x: Any) -> float:

    return float(x) if x is not None else float(0)


def from_str(x: Any) -> str:
    if str(x) in ["None", "none"]:
        return None

    return str(x)


def from_bool(x: Any) -> bool:

    return bool(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:

    return [f(y) for y in x] if x is not None else []


def from_datetime(x: Any) -> datetime:
    x = x or "2019-01-01"
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


__all__ = get_all(locals())
