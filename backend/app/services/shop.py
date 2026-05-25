from typing import type_check_only
from app.db.models.shop import Shop
from app.db.repositories.shop_repository import ShopRepository
from app.schemas import shop
from app.schemas.shop import (ShopCreateDTO, ShopListDTO, 
                                 ShopUpdateDTO, ShopViewDTO)
from app.services.exceptions import ShopAlreadyExistsError, ShopNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


class ShopService:
    def __init__(self, session: AsyncSession, shop_repository: ShopRepository):

        self.session = session
        self.shop_repository = shop_repository


    async def create_shop(self, schema: ShopCreateDTO) -> ShopViewDTO:
       
        shop = await self.shop_repository.get_by_phone_number(schema.phone_number)
        if shop is not None:
            raise ShopAlreadyExistsError(schema.phone_number)

        shop = Shop(
            name=schema.name,
            address=schema.address,
            contact_face=schema.contact_face,
            phone_number=schema.phone_number,
            email=schema.email
        )

        async with self.session.begin():
            shop = await self.shop_repository.save(shop)

        return ShopViewDTO.model_validate(shop)


    async def get_by_id(self, id: int) -> ShopViewDTO:

        shop = await self.shop_repository.get_by_id(id)
        
        if shop is None:
            raise ShopNotFoundError(id)

        return ShopViewDTO.model_validate(shop)


    async def get_all(self) -> ShopListDTO:

        shops = await self.shop_repository.get_all()

        return ShopListDTO(
            count=len(shops),
            items=[ShopViewDTO.model_validate(shop) for shop in shops]
        )


    async def delete(self, id: int) -> None:
        
        shop = await self.shop_repository.get_by_id(id)
        
        if shop is None:
            raise ShopNotFoundError(id)

        async with self.session.begin():
            await self.shop_repository.delete(shop)
    

    async def update(self, schema: ShopUpdateDTO) -> ShopViewDTO:

        shop = await self.shop_repository.get_by_phone_number(
            schema.phone_number
        )
        if shop is None:
            raise ShopNotFoundError(schema.id)

        if shop is not None and shop.id != schema.id:
            raise ShopAlreadyExistsError(schema.phone_number)

        shop.name = schema.name
        shop.address = schema.address
        shop.contact_face = schema.contact_face
        shop.phone_number = schema.phone_number
        shop.email = schema.email

        async with self.session.begin():
            shop = await self.shop_repository.save(shop)

        return ShopViewDTO.model_validate(shop) 
