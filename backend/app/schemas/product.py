from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductView(BaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductUpdate(BaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductList(BaseModel):
    count: int
    items: list[ProductView]
