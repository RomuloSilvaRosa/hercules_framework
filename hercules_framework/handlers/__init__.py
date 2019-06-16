
import json
from http import HTTPStatus
from typing import Dict, List, Union

import tornado.web
# import sys; import hercules_framework; sys.path.insert(0, hercules_framework.settings.APP_FOLDER)  # NOQA
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonValidationError

from hercules_framework.logger import get_logger
from hercules_framework.models.base import BaseModel, check_type
from hercules_framework.models.response import Response
from hercules_framework.exceptions.base import HerculesException


class BaseHandler(tornado.web.RequestHandler):
    # Dict with client's data coming from request
    request_body = {}
    json_schema_model = None
    json_schema_model: str = None
    logger = None

    def data_received(self, chunk: object) -> None:
        pass

    async def prepare(self) -> Union[object, None]:
        """
        This method is executed before all requests, after initialize.
        - It will be used to execute all common routines.
        """
        self.logger = get_logger()
        try:
            if not self.request.body:
                self.request_body = {}
            else:
                self.request_body = json.loads(self.request.body)

            # Executed all request validations
            self.validate_request()
        except Exception as exc:
            return self._treat_general_exception(exception=exc)

    def _treat_general_exception(self, exception: Exception):
        print('treating')
        self.logger.exception(exception)
        status = exception.http_status if issubclass(type(exception), HerculesException) \
            else HTTPStatus.INTERNAL_SERVER_ERROR
        self.send_response(code=status,
                           data={'error': str(exception)},
                           message=str(exception))

    def write_response(self,
                       http_status: int,
                       description: str,
                       response_body: Union[Dict, List, str, bytes] = None,
                       log_level: str = None,
                       extra: Dict = None,
                       http_status_reason: str = ''
                       ) -> None:

        # HTTP headers
        headers = ['Content-Type', 'application/json; charset=utf-8']
        self.set_header(*headers)

        # HTTP status
        self.set_status(http_status, http_status_reason)

        # HTTP Body
        response_body_parsed = None
        if response_body is not None:
            if isinstance(response_body, str):
                response_body_parsed = response_body
            elif isinstance(response_body, bytes):
                response_body_parsed = response_body.decode()
            else:
                response_body_parsed = json.dumps(
                    response_body, ensure_ascii=False)
        if response_body_parsed is not None:
            self.write(response_body_parsed)
        self.finish()

    def get_query_args(self) -> dict:
        args: dict = self.request.arguments
        for key, value in args.items():
            if len(value) == 1 and isinstance(value, list):
                args[key] = self.decode_argument(value[0])
            else:
                args[key] = [self.decode_argument(
                    each_item) for each_item in value]
        return args

    def send_response(self, message: str=None, data: dict = None,
                      description: str="Ok", code: int=HTTPStatus.OK):
        if not isinstance(data, dict) and data:
            if issubclass(type(data), BaseModel):
                data: BaseModel
                data = data.to_dict()
            else:
                try:
                    data = json.loads(data)
                except:
                    pass
                check_type([dict, list], data=data)
        resp = Response(data=data, message=message or "Ok", code=code)
        self.write_response(http_status=code, description=description,
                            response_body=resp.to_dict())

    def validate_request(self):
        if self.request.method in ['POST', 'PUT']:
            status = HTTPStatus.UNPROCESSABLE_ENTITY
            resp = "Error in schema validation"
            if self.json_schema_model:
                try:
                    validate(instance=self.request_body,
                             schema=self.json_schema_model)
                except JsonValidationError as error:
                    error: JsonValidationError
                    self.logger.exception(error)
                    self.send_response(code=status, description=resp,
                                       message='{}: {}'.format(resp, error.message))


class HealthCheckHandler(BaseHandler):

    async def get(self):
        self.send_response()


def run_method_safe(func):

    async def func_wrapper(self, *args, **kwargs):
        self: BaseHandler

        try:
            return await func(self, *args, **kwargs)
        except Exception as exc:
            self.logger.exception(exc)
            return self._treat_general_exception(exception=exc)

    return func_wrapper
