import datetime
from functools import wraps

import jwt
from passlib.context import CryptContext

from hercules_framework.exceptions.auth import AuthException
from hercules_framework.handlers import BaseHandler

from hercules_framework.settings import AUTH_CRYPT_KEY


class JwTAuth:
    _pwd_context = CryptContext(
        schemes=['pbkdf2_sha256'])

    @classmethod
    def encrypt_password(cls, password: str):
        return cls._pwd_context.encrypt(password)

    def check_encrypted_password(cls, password: str, hashed: str):
        return cls._pwd_context.verify(password, hashed)

    @staticmethod
    def generate_auth_token(username: str):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                'sub': {
                    'username': username,
                }
            }
            token = jwt.encode(payload, AUTH_CRYPT_KEY, algorithm='HS256')
            return token.decode()
        except Exception as e:
            return e

    @classmethod
    def decode_auth_token(cls, token: str) -> None:
        payload = jwt.decode(token, AUTH_CRYPT_KEY)
        return payload['sub']


def tornado_auth_token_required(func):
    @wraps(func)
    async def decorated(self, *args, **kwargs):
        self: BaseHandler
        try:
            token = self.request.headers.get('Authorization', None)
            # exit(0)
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

def flask_auth_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)

        if not token:
            abort(403, 'Token não especificado no header')
        _, jwt_token = token.split()
        JwTAuth.decode_auth_token(jwt_token)
        return func(*args, **kwargs)