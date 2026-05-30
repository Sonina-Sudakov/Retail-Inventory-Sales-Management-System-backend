from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBaseModel):
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductView(ProductBaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductUpdate(ProductBaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductList(ProductBaseModel):
    count: int
    items: list[ProductView]
