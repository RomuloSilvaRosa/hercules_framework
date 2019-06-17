from hercules_framework.models.crud_response import (ClientModel, OrderModel,
                                                     SellerModel)
from hercules_framework.settings import CRUD_CLIENT_HOST, CRUD_ORDER_HOST, CRUD_SELLER_HOST
from .base import BaseTalker


class SellerTalker(BaseTalker):
    base_url = 'hercules/crud-seller/v1/seller'
    model = SellerModel

    def __init__(self, host: str=CRUD_SELLER_HOST):
        self.host = host


class OrderTalker(BaseTalker):
    base_url = 'hercules/crud-order/v1/order'
    model = OrderModel

    def __init__(self, host: str=CRUD_ORDER_HOST):
        self.host = host


class CLientTalker(BaseTalker):
    base_url = 'hercules/crud-client/v1/client'
    model = ClientModel

    def __init__(self, host: str=CRUD_CLIENT_HOST):
        self.host = host
