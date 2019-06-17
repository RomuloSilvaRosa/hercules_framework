
from dataclasses import dataclass
from uuid import UUID

from dataslots import with_slots

from .base import *


@with_slots
@dataclass
class OrderModel:
    order_id: UUID
    client_id: UUID
    seller_id: UUID
    order_price: int
    order_discount: int

    @staticmethod
    def from_dict(obj: Any) -> 'OrderModel':
        assert isinstance(obj, dict)
        order_id = UUID(obj.get("orderId"))
        client_id = UUID(obj.get("clientId"))
        seller_id = UUID(obj.get("sellerId"))
        order_price = from_int(obj.get("orderPrice"))
        order_discount = from_int(obj.get("orderDiscount"))
        return OrderModel(order_id, client_id, seller_id, order_price, order_discount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["orderId"] = str(self.order_id)
        result["clientId"] = str(self.client_id)
        result["sellerId"] = str(self.seller_id)
        result["orderPrice"] = from_int(self.order_price)
        result["orderDiscount"] = from_int(self.order_discount)
        return result


@with_slots
@dataclass
class SellerModel(BaseModel):
    id: UUID
    vehicle_type: str
    district: int

    @staticmethod
    def from_dict(obj: Any) -> 'SellerModel':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        vehicle_type = from_str(obj.get("vehicleType"))
        district = from_int(obj.get("district"))
        return SellerModel(id, vehicle_type, district)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["vehicleType"] = from_str(self.vehicle_type)
        result["district"] = from_int(self.district)
        return result


@with_slots
@dataclass
class ClientModel(BaseModel):
    id: UUID
    client_type: str
    cnpj: str
    district: int
    satisfation_score: int
    created_at: str
    updated_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'ClientModel':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        client_type = from_str(obj.get("clientType"))
        cnpj = from_str(obj.get("cnpj"))
        district = from_int(obj.get("district"))
        satisfation_score = from_int(obj.get("satisfationScore"))
        created_at = from_str(obj.get("createdAt"))
        updated_at = from_str(obj.get("updatedAt"))
        return ClientModel(id, client_type, cnpj, district, satisfation_score, created_at, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["clientType"] = from_str(self.client_type)
        result["cnpj"] = from_str(self.cnpj)
        result["district"] = from_int(self.district)
        result["satisfationScore"] = from_int(self.satisfation_score)
        result["createdAt"] = from_str(self.created_at)
        result["updatedAt"] = from_str(self.updated_at)
        return result


@dataclass
class CRUDResponse(BaseModel):
    message: str
    data: List[BaseModel]

    @staticmethod
    def from_dict(obj: Any, data_model: BaseModel) -> 'CRUDResponse':
        message = from_str(obj.get("message"))
        data = from_list(data_model.from_dict, obj.get("data", []))
        return CRUDResponse(message, data)

    def to_dict(self, data_model: BaseModel) -> dict:
        result: dict = {}
        return result
