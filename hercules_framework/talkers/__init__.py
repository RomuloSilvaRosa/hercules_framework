from typing import Union

from hercules_framework.models.base import BaseModel
from hercules_framework.models.crud_response import (ClientModel, OrderModel,
                                                     SellerModel)
from hercules_framework.settings import (CRUD_CLIENT_HOST, CRUD_ORDER_HOST,
                                         CRUD_SELLER_HOST)

from .base import BaseTalker, session


class SellerTalker(BaseTalker):
    base_url = 'hercules/crud-seller/v1/seller'
    model = SellerModel

    def __init__(self, host: str = CRUD_SELLER_HOST):
        self.host = host


class OrderTalker(BaseTalker):
    base_url = 'hercules/crud-order/v1/order'
    model = OrderModel

    def __init__(self, host: str = CRUD_ORDER_HOST):
        self.host = host

    def get(self, id: str, header: dict = {}, first=True) -> Union[BaseModel, None]:
        header.update(self._base_header)
        url = '/'.join([self.host, self.base_url, '']) + f'?orderId={id}'
        response: Response = session.get(
            url=url, headers=header)
        return self._treat_response(response.json(), first=first)


class CLientTalker(BaseTalker):
    base_url = 'hercules/crud-client/v1/client'
    model = ClientModel

    def __init__(self, host: str = CRUD_CLIENT_HOST):
        self.host = host
