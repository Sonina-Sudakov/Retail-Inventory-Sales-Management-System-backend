from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreateDTO(BaseModel):
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductViewDTO(BaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductUpdateDTO(BaseModel):
    id: int
    name: str
    unit: str
    type_: str = Field(alias='type')
    price: Decimal 
    origin: str


class ProductListDTO(BaseModel):
    count: int
    items: list[ProductViewDTO]
