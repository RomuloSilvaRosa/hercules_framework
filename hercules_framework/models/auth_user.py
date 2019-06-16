from dataclasses import dataclass

from dataslots import with_slots

from hercules_framework.models.base import *


@with_slots
@dataclass
class AuthUserModel(BaseModel):
    username: str
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'AuthUserModel':
        # assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        password = from_str(obj.get("password"))
        return AuthUserModel(username, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["username"] = from_str(self.username)
        result["password"] = from_str(self.password)
        return result


def indexing_from_dict(s: Any) -> AuthUserModel:
    return AuthUserModel.from_dict(s)


def indexing_to_dict(x: AuthUserModel) -> Any:
    return to_class(AuthUserModel, x)
