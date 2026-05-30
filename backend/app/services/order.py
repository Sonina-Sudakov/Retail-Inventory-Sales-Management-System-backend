from sqlalchemy.orm.strategy_options import selectinload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.repositories.order import OrderRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.product import ProductRepository
from app.db.repositories.user import UserRepository
from app.enums import OrderStatus
from app.schemas.order import (OrderCreate, OrderDetailedView, OrderList,
                               OrderView)
from app.services.exceptions import (EmptyOrderError, OrderNotFoundError,
                                     ProductNotFoundError, ShopNotFoundError,
                                     UserNotFoundError)


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

        shop = await self.shop_repository.get_by_id(schema.shop_id)

        if shop is None:
            raise ShopNotFoundError(schema.shop_id)

        user = await self.user_repository.get_by_id(schema.created_by_id)

        if user is None:
            raise UserNotFoundError(schema.created_by_id)

        for item in schema.items:

            product = await self.product_repository.get_by_id(item.product_id)

            if product is None:
                raise ProductNotFoundError(item.product_id)

        order = Order(
            shop_id=schema.shop_id,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity                    
                )
                for item in schema.items
            ]
        )

        order = await self.order_repository.save(order)

        return OrderView.model_validate(order)


    async def get_by_id(self, id: int) -> OrderDetailedView:

        order = await self.order_repository.get_by_id(
            id,
            options=[selectinload(Order.items)]
        )
        
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

        orders = await self.order_repository.get_all()

        return OrderList(
            count=len(orders),
            items=[OrderView.model_validate(order) for order in orders]
        )


    async def update_status(self, id: int, status: OrderStatus) -> OrderView:

        
        order = await self.order_repository.get_by_id(id)

        if order is None:
            raise OrderNotFoundError(id)

        order.status = status

        order = await self.order_repository.save(order)

        return OrderView.model_validate(order)
