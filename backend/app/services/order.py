from datetime import datetime, timezone

from sqlalchemy.orm.strategy_options import selectinload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.user import User
from app.db.repositories.order import OrderRepository
from app.db.repositories.product import ProductRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.enums import OrderStatus
from app.schemas.order import (OrderCreate, OrderDetailedView, OrderList,
                               OrderView)
from app.services.exceptions import (EmptyOrderError, OrderIsNotPendingError,
                                     OrderNotFoundError, ProductNotFoundError,
                                     ShopNotFoundError, UserNotFoundError)


class OrderService:
    def __init__(
            self, 
            order_repository: OrderRepository, 
            shop_repository: ShopRepository,
            product_repository: ProductRepository,
            user_repository: UserRepository
        ):
        
        self.order_repository = order_repository
        self.shop_repository = shop_repository
        self.product_repository = product_repository
        self.user_repository = user_repository


    async def create_order(self, schema: OrderCreate) -> OrderView:
      
        if not schema.items:
            raise EmptyOrderError() 

        shop = await self.shop_repository.get_by_id(schema.to_shop_id)

        if shop is None:
            raise ShopNotFoundError(schema.to_shop_id)

        user = await self.user_repository.get_by_id(schema.created_by_id)

        if user is None:
            raise UserNotFoundError(schema.created_by_id)

        for item in schema.items:

            product = await self.product_repository.get_by_id(item.product_id)

            if product is None:
                raise ProductNotFoundError(item.product_id)

        order = Order(
            to_shop_id=schema.to_shop_id,
            created_by_id=schema.created_by_id,
            
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity                    
                )
                for item in schema.items
            ]
        )

        order = await self.order_repository.save(order)

        order = await self.load_order_(order.id)

        return OrderView.model_validate(order)


    async def get_by_id(self, id: int) -> OrderDetailedView:

        order = await self.load_order_with_products_(id)
        
        if order is None:
            raise OrderNotFoundError(id)

        return OrderDetailedView.model_validate(order)


    async def get_by_shop(self, shop_id: int) -> OrderList:

        orders = await self.order_repository.get_shop_orders(shop_id)
        
        return OrderList(
            count=len(orders),
            items=[OrderView.model_validate(order) for order in orders]
        )


    async def get_by_status(self, status: OrderStatus) -> OrderList:

        orders = await self.order_repository.get_orders_by_status(status)
        
        return OrderList(
            count=len(orders),
            items=[OrderView.model_validate(order) for order in orders]
        )


    async def get_all(self) -> OrderList:

        orders = await self.order_repository.get_all(
            options=[
                selectinload(Order.created_by),
                selectinload(Order.to_shop)
            ]
        )

        return OrderList(
            count=len(orders),
            items=[OrderView.model_validate(order) for order in orders]
        )


    async def accept_order(self, id: int) -> OrderView:

        order = await self.order_repository.get_by_id(id)

        if order is None:
            raise OrderNotFoundError(id)

        if order.status != OrderStatus.PENDING:
            raise OrderIsNotPendingError(id)

        order = await self.update_status_(order, OrderStatus.ACCEPTED)

        return order


    async def cancel_order(self, id: int) -> OrderView:

        order = await self.order_repository.get_by_id(id)

        if order is None:
            raise OrderNotFoundError(id)

        if order.status != OrderStatus.PENDING:
            raise OrderIsNotPendingError(id)

        return await self.update_status_(order, OrderStatus.CANCELED)
    

    async def update_status_(self, model: Order, status: OrderStatus) -> OrderView:

        if status == OrderStatus.ACCEPTED:
            model.accepted_at = datetime.now(timezone.utc)

        model.status = status

        await self.order_repository.save(model)

        return OrderView.model_validate(await self.load_order_(model.id))


    async def load_order_(
        self,
        id: int
    ) -> Order:

        model = await self.order_repository.get_by_id(
            id,
            options=[
                selectinload(Order.to_shop),
                selectinload(Order.created_by).selectinload(User.works_in_shop),
                selectinload(Order.items)
            ]
        )

        if not model:
            raise OrderNotFoundError(id)

        return model


    async def load_order_with_products_(
        self,
        id: int
    ) -> Order:

        model = await self.order_repository.get_by_id(
            id,
            options=[
                selectinload(Order.to_shop),
                selectinload(Order.created_by).selectinload(User.works_in_shop),
                selectinload(Order.items).selectinload(OrderItem.product)
            ]
        )

        if not model:
            raise OrderNotFoundError(id)

        return model
