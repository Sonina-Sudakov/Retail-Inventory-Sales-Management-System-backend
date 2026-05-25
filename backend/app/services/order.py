from typing import type_check_only

from sqlalchemy.orm.strategy_options import selectinload
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.repositories import shop_repository
from app.db.repositories.order_repository import OrderRepository
from app.db.repositories.shop_repository import ShopRepository
from app.schemas.order import (OrderCreateDTO, OrderDetailedViewDTO, OrderListDTO, 
                                 OrderViewDTO)
from app.enums import OrderStatus

from app.services.exceptions import EmptyOrderError, OrderNotFoundError, ShopNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


class OrderService:
    def __init__(self, session: AsyncSession, order_repository: OrderRepository):

        self.session = session
        self.order_repository = order_repository
        self.shop_repository = shop_repository


    async def create_order(self, schema: OrderCreateDTO) -> OrderViewDTO:
      
        if not schema.items:
            raise EmptyOrderError()

        order = Order(
            shop_id=schema.shop_id
        )

        shop = await self.shop_repository.get_by_id(schema.shop_id)

        if shop is None:
            raise ShopNotFoundError(schema.shop_id)

        async with self.session.begin():
            order = await self.order_repository.save(order)

            for item in schema.items:
                await self.order_repository.save_order_item(
                    OrderItem(
                        order_id=order.id,
                        product_id=item.product_id,
                        quantity=item.quantity                    
                    )
                )

        return OrderViewDTO.model_validate(order)


    async def get_by_id(self, id: int) -> OrderDetailedViewDTO:

        order = await self.order_repository.get_by_id(
            id,
            options=[selectinload(Order.items)]
        )
        
        if order is None:
            raise OrderNotFoundError(id)

        return OrderDetailedViewDTO.model_validate(order)


    async def get_by_shop(self, shop_id: int) -> OrderListDTO:

        orders = await self.order_repository.get_shop_orders(shop_id)
        
        return OrderListDTO(
            count=len(orders),
            items=[OrderViewDTO.model_validate(order) for order in orders]
        )


    async def get_by_status(self, status: OrderStatus) -> OrderListDTO:

        orders = await self.order_repository.get_orders_by_status(status)
        
        return OrderListDTO(
            count=len(orders),
            items=[OrderViewDTO.model_validate(order) for order in orders]
        )


    async def get_all(self) -> OrderListDTO:

        orders = await self.order_repository.get_all()

        return OrderListDTO(
            count=len(orders),
            items=[OrderViewDTO.model_validate(order) for order in orders]
        )


    async def update_status(self, id: int, status: OrderStatus) -> OrderViewDTO:

        
        order = await self.order_repository.get_by_id(id)

        if order is None:
            raise OrderNotFoundError(id)

        order.status = status

        async with self.session.begin():
            order = await self.order_repository.save(order)

        return OrderViewDTO.model_validate(order)
