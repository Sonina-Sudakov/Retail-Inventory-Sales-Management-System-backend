from sqlalchemy.exc import IntegrityError

from app.db.models.shop import Shop
from app.db.repositories.shop import ShopRepository
from app.schemas.shop import ShopCreate, ShopList, ShopUpdate, ShopView
from app.services.exceptions import ShopAlreadyExistsError, ShopNotFoundError


class ShopService:
    def __init__(self, shop_repository: ShopRepository):

        self.shop_repository = shop_repository


    async def create_shop(self, schema: ShopCreate) -> ShopView:
       
        try:
            shop = Shop(
                name=schema.name,
                address=schema.address,
                contact_face=schema.contact_face,
                phone_number=schema.phone_number,
                email=schema.email
            )

            shop = await self.shop_repository.save(shop)

            return ShopView.model_validate(shop)
        except IntegrityError:
            raise ShopAlreadyExistsError(schema.phone_number, schema.email)


    async def get_by_id(self, id: int) -> ShopView:

        shop = await self.shop_repository.get_by_id(id)
        
        if shop is None:
            raise ShopNotFoundError(id)

        return ShopView.model_validate(shop)


    async def get_all(self) -> ShopList:

        shops = await self.shop_repository.get_all()

        return ShopList(
            count=len(shops),
            items=[ShopView.model_validate(shop) for shop in shops]
        )


    async def delete(self, id: int) -> None:
        
        shop = await self.shop_repository.get_by_id(id)
        
        if shop is None:
            raise ShopNotFoundError(id)

        await self.shop_repository.delete(shop)
    

    async def update(self, schema: ShopUpdate) -> ShopView:

        try:
            shop = await self.shop_repository.get_by_id(schema.id)

            if shop is None:
                raise ShopNotFoundError(schema.id)

            shop.name = schema.name
            shop.address = schema.address
            shop.contact_face = schema.contact_face
            shop.phone_number = schema.phone_number
            shop.email = schema.email

            shop = await self.shop_repository.save(shop)
        except IntegrityError:
            raise ShopAlreadyExistsError(schema.phone_number, schema.email)

        return ShopView.model_validate(shop) 
