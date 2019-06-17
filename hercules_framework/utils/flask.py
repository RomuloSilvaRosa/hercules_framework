from functools import wraps
from http import HTTPStatus

from flask import abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response

from hercules_framework.models.response import Response
from hercules_framework.jwt.jwt_auth import JwTAuth


def log_body(function):
    def wrap_function(*args, **kwargs):
        body = request.get_json()
        kwargs.update(body=body)
        return function(*args, **kwargs)
    wrap_function.__name__ = function.__name__  # avoid flask view errors
    return wrap_function


def send_ok_response(msg=None, data: dict = None, status: int = None) -> Response:
    status = status or HTTPStatus.OK
    msg or "Ok"
    resp = Response(message=msg, data=data, code=status)
    response = jsonify(resp.to_dict())
    response.status_code = status
    return response


def send_error_response(error: Exception = None, status=None):
    status = status or HTTPStatus.INTERNAL_SERVER_ERROR
    app.logger.exception(error)
    resp = Response(message=str(error), code=status)
    response = jsonify(resp.to_dict())
    response.status_code = status
    return response


def flask_auth_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        try:
            if not token:
                abort(403, 'Token não especificado no header')
            _, jwt_token = token.split()
            JwTAuth.decode_auth_token(jwt_token)
        except:
            abort(401, 'Token invalido')
        return func(*args, **kwargs)
    return decorated
