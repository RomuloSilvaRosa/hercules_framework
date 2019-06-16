
from dataclasses import dataclass

from dataslots import with_slots

from hercules_framework.models.base import *


@with_slots
@dataclass
class DataModel:
    score_cspa: int
    age: int
    value_total_order: int
    total_installments_order: int
    declared_income_order: int
    uf_order: int
    profession_name: str
    occupation_name: str
    value_car: int
    city_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'DataModel':
        assert isinstance(obj, dict)
        score_cspa = from_int(obj.get("score_cspa"))
        age = from_int(obj.get("age"))
        value_total_order = int(from_str(obj.get("value_total_order")))
        total_installments_order = int(
            from_str(obj.get("total_installments_order")))
        declared_income_order = int(from_str(obj.get("declared_income_order")))
        uf_order = from_int(obj.get("uf_order"))
        profession_name = from_str(obj.get("profession_name"))
        occupation_name = from_str(obj.get("occupation_name"))
        value_car = int(from_str(obj.get("value_car")))
        city_name = from_str(obj.get("city_name"))
        return DataModel(score_cspa, age, value_total_order, total_installments_order, declared_income_order, uf_order, profession_name, occupation_name, value_car, city_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["score_cspa"] = from_int(self.score_cspa)
        result["age"] = from_int(self.age)
        result["value_total_order"] = from_str(str(self.value_total_order))
        result["total_installments_order"] = from_str(
            str(self.total_installments_order))
        result["declared_income_order"] = from_str(
            str(self.declared_income_order))
        result["uf_order"] = from_int(self.uf_order)
        result["profession_name"] = from_str(self.profession_name)
        result["occupation_name"] = from_str(self.occupation_name)
        result["value_car"] = from_str(str(self.value_car))
        result["city_name"] = from_str(self.city_name)
        return result


def data_model_from_dict(s: Any) -> DataModel:
    return DataModel.from_dict(s)


def data_model_to_dict(x: DataModel) -> Any:
    return to_class(DataModel, x)
