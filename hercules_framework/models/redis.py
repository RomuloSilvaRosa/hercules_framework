
from dataclasses import dataclass

from .base import *


@dataclass
class Cache(BaseModel):
    host: str
    port: int
    db: str

    @staticmethod
    def from_dict(obj: Any) -> 'Cache':
        host = from_str(obj.get("host"))
        port = from_int(obj.get("port"))
        db = from_str(obj.get("db"))
        return Cache(host, port, db)

    def to_dict(self) -> dict:
        result: dict = {}
        result["host"] = from_str(self.host)
        result["port"] = from_int(self.port)
        result["db"] = from_str(self.db)
        return result


def cache_from_dict(s: Any) -> Cache:
    return Cache.from_dict(s)


def cache_to_dict(x: Cache) -> Any:
    return to_class(Cache, x)
