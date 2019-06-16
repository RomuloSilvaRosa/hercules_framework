from http import HTTPStatus

from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response

from hercules_framework.models.response import Response


def log_body(function):
    def wrap_function(*args, **kwargs):
        body = request.get_json()
        kwargs.update(body=body)
        return function(*args, **kwargs)
    wrap_function.__name__ = function.__name__  # avoid flask view errors
    return wrap_function


def send_ok_response(msg=None, data: dict=None, status: int=None) -> Response:
    status = status or HTTPStatus.OK
    msg or "Ok"
    resp = Response(message=msg, data=data, code=status)
    print(resp)
    response = jsonify(resp.to_dict())
    response.status_code = status
    return response


def send_error_response(error: Exception=None, status=None):
    status = status or HTTPStatus.INTERNAL_SERVER_ERROR
    app.logger.exception(error)
    resp = Response(message=str(error), code=status)
    response = jsonify(resp.to_dict())
    response.status_code = status 
    return response
