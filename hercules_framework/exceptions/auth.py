from .base import HerculesException

class AuthException(HerculesException):
    http_status = 403
    def __init__(self,status:int=403, *args, **kwargs):
        self.http_status = status
        super().__init__(*args, **kwargs)
