import datetime

import jwt
from passlib.context import CryptContext

from hercules_framework.settings import AUTH_CRYPT_KEY


class JwTAuth:
    _pwd_context = CryptContext(
        schemes=['pbkdf2_sha256'])

    @classmethod
    def encrypt_password(cls, password: str):
        return cls._pwd_context.encrypt(password)

    @classmethod
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





