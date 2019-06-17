from functools import wraps

from hercules_framework.exceptions.auth import AuthException
from hercules_framework.handlers import BaseHandler
from hercules_framework.security.jwt_auth import JwTAuth


def tornado_auth_token_required(func):
    @wraps(func)
    async def decorated(self, *args, **kwargs):
        self: BaseHandler
        try:
            token = self.request.headers.get('Authorization', None)
            if token is None:
                raise AuthException(403, 'Token not found')
            try:
                _, jwt_token = token.split()
                JwTAuth.decode_auth_token(jwt_token)
            except Exception:
                raise AuthException(401, 'Expired or invalid token')
        except Exception as exc:
            self._treat_general_exception(exc)
        return await func(self, *args, **kwargs)
    return decorated
