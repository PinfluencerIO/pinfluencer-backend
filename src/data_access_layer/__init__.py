import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

PRODUCT_TBL_NAME = 'product'
BRAND_TBL_NAME = 'brand'


def uuid4_str():
    return str(uuid.uuid4())


@dataclass
class BaseEntity:
    id: str = Column(String(length=36), primary_key=True, default=uuid4_str, nullable=False)
    created: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "created": self.created
        }


Base = declarative_base()


def to_list(data):
    data_dict = []
    for data_item in data:
        data_dict.append(data_item.as_dict())
    return data_dict


class ValueEnum(Enum):
    Sustainable = "Sustainable"
    Organic = "Organic"
    Recycled = "Recycled"
    Vegan = "Vegan"
    Value5 = "Value5"
    Value6 = "Value6"
    Value7 = "Value7"
    Value8 = "Value8"
    Value9 = "Value9"
    Value10 = "Value10"


class CategoryEnum(Enum):
    Food = "Food"
    Fashion = "Fashion"
    Fitness = "Fitness"
    Pet = "Pet"
    Category5 = "Category5"
    Category6 = "Category6"
    Category7 = "Category7"
    Category8 = "Category8"
    Category9 = "Category9"
    Category10 = "Category10"


class BaseUser(BaseEntity):
    first_name: str = Column(type_=String(length=120), nullable=False)
    last_name: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)

    def as_dict(self):
        dict = super().as_dict()
        dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "auth_user_id": self.auth_user_id
        })
        return dict
