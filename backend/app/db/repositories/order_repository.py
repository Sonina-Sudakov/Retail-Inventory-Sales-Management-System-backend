from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.shop import Shop
from app.db.repositories.base_repository import BaseRepository
from enums import OrderStatus


class OrderRepository(
    BaseRepository[Order]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Order, session)


    async def get_shop_orders(
        self,
        shop_id: int
    ) -> list[Order]:
        
        stmt = select(Order).where(Order.to_shop_id == shop_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def get_user_orders(
        self,
        user_id: int
    ) -> list[Order]:

        stmt = select(Order).where(Order.created_by_id == user_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def get_full_order_by_id(
        self,
        id: int
    ) -> Order | None:
        
        order = await self.get_by_id(
            id,
            options=[
                selectinload(Order.shop),
                selectinload(Order.order_items)
            ]
        )

        return order

   
    async def get_orders_by_status(
        self,
        status: OrderStatus
    ) -> list[Order]:

        stmt = (
            select(
                Order,
                Shop.name,
                Shop.address
            )
            .join(Shop)
            .where(Order.status == status)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())   


    async def save_order_item(
        self,
        entity: OrderItem
    ) -> None:

        self.session.add(entity)

        await self.session.flush()
