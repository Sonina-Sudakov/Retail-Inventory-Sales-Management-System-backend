from typing import type_check_only

from sqlalchemy.orm.strategy_options import selectinload
from app.db.models.sale import Sale
from app.db.models.sale_item import SaleItem
from app.db.repositories.sale_repository import SaleRepository
from app.schemas.sale import (SaleCreateDTO, SaleDetailedViewDTO, SaleListDTO, 
                                 SaleUpdateDTO, SaleViewDTO)
from app.services.exceptions import SaleAlreadyExistsError, SaleNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


class SaleService:
    def __init__(self, session: AsyncSession, sale_repository: SaleRepository):

        self.session = session
        self.sale_repository = sale_repository


    async def create_sale(self, schema: SaleCreateDTO) -> SaleViewDTO:
      
        if not schema.items:
            raise EmptySaleError()

        sale = Sale(
            shop_id=schema.shop_id,
            user_id=schema.user_id
        )

        async with self.session.begin():
            sale = await self.sale_repository.save(sale)

            for item in schema.items:
                await self.sale_repository.save_sale_item(
                    SaleItem(
                        sale_id=sale.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price
                    )
                )

        return SaleViewDTO.model_validate(sale)


    async def get_by_id(self, id: int) -> SaleDetailedViewDTO:

        sale = await self.sale_repository.get_by_id(
            id,
            options=[selectinload(Sale.items)]
        )
        
        if sale is None:
            raise SaleNotFoundError(id)

        return SaleDetailedViewDTO.model_validate(sale)


    async def get_by_shop(self, shop_id: int) -> SaleListDTO:

        sales = await self.sale_repository.get_shop_sales(shop_id)
        
        return SaleListDTO(
            count=len(sales),
            items=[SaleViewDTO.model_validate(sale) for sale in sales]
        )

    async def get_all(self) -> SaleListDTO:

        sales = await self.sale_repository.get_all()

        return SaleListDTO(
            count=len(sales),
            items=[SaleViewDTO.model_validate(sale) for sale in sales]
        )

