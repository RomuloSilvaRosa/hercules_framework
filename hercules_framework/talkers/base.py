from typing import Union

import requests
from requests import Response

from hercules_framework.models.crud_response import BaseModel, CRUDResponse


class BaseTalker:
    base_url: str = None
    host: str = None
    model: BaseModel = None
    _base_header = {'Content-Type': 'application/json'}

    def get(self, id: str, header: dict = {}, first=True) -> Union[BaseModel, None]:
        header.update(self._base_header)
        url = '/'.join([self.host, self.base_url, str(id)])
        response: Response = requests.get(url=url + '?limit=1', headers=header)
        json_response = response.json()
        if json_response is not None:
            resp = CRUDResponse.from_dict(json_response, self.model).data
            if first:
                return resp[0] if len(resp) else None
            return resp
        return None

    def put(self, body: dict, header: dict = {}) -> int:
        header.update(self._base_header)
        url = '/'.join([self.host, self.base_url])
        response: Response = requests.post(url=url, json=body, headers=header)
        return response.status_code
