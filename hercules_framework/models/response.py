
from dataclasses import dataclass, field

from .base import *

from dataslots import with_slots
@with_slots
@dataclass
class Response(BaseModel):
    message: str
    data: dict = field(default=None)
    code: int = field(default=None)

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        # assert isinstance(obj, dict)
        data = obj.get("data")
        message = from_str(obj.get("message"))
        code = from_str(obj.get("code"))
        return Response(data, code, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = self.data
        result["message"] = from_str(self.message)
        result["code"] = from_int(self.code)
        return result


def response_from_dict(s: Any) -> Response:
    return Response.from_dict(s)


def response_to_dict(x: Response) -> Any:
    return to_class(Response, x)
