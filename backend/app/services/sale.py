from sqlalchemy.orm.strategy_options import selectinload

from app.db.models.sale import Sale
from app.db.models.sale_item import SaleItem
from app.db.repositories.product import ProductRepository
from app.db.repositories.sale import SaleRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.schemas.sale import (SaleCreate, SaleDetailedView, SaleItemView,
                              SaleList, SaleView)
from app.schemas.shop_stock import UpdateShopStockQuantity
from app.services.exceptions import (EmptySaleError, ProductNotFoundError,
                                     SaleNotFoundError, ShopNotFoundError,
                                     UserNotFoundError)
from app.services.shop_stock import ShopStockService


class SaleService:
    def __init__(
            self, 
            sale_repository: SaleRepository,
            shop_repository: ShopRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository,
            shop_stock_service: ShopStockService
        ):

        self.sale_repository = sale_repository
        self.shop_repository = shop_repository
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.shop_stock_service = shop_stock_service


    async def create_sale(self, schema: SaleCreate) -> SaleView:
      
        if not schema.items:
            raise EmptySaleError()

        shop = await self.shop_repository.get_by_id(schema.shop_id)
        
        if shop is None:
            raise ShopNotFoundError(schema.shop_id)

        user = await self.user_repository.get_by_id(schema.user_id)

        if user is None:
            raise UserNotFoundError(schema.user_id)

        for item in schema.items:

            product = await self.product_repository.get_by_id(item.product_id)

            if product is None:
                raise ProductNotFoundError(item.product_id)

            await self.shop_stock_service.decrease_stock_quantity(
                UpdateShopStockQuantity(
                    shop_id=schema.shop_id,
                    product_id=item.product_id,
                    change=item.quantity
                )
            )

        sale = Sale(
            shop_id=schema.shop_id,
            user_id=schema.user_id,
            items=[
                SaleItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )
                for item in schema.items
            ]
        )

        sale = await self.sale_repository.save(sale)

        sale = await self.sale_repository.get_by_id(
            sale.id,
            options=[
                selectinload(Sale.shop),
                selectinload(Sale.user),
                selectinload(Sale.items)
            ]
        )

        return SaleView.model_validate(sale)


    async def get_by_id(self, id: int) -> SaleDetailedView:

        sale = await self.sale_repository.get_by_id(
            id,
            options=[
                selectinload(Sale.shop),
                selectinload(Sale.user),
                selectinload(Sale.items).selectinload(SaleItem.product)
            ]
        )
        
        if sale is None:
            raise SaleNotFoundError(id)

        return SaleDetailedView(
            id=sale.id,
            shop=sale.shop,
            user=sale.user,
            count=len(sale.items),
            items=[
                SaleItemView.model_validate(item)
                for item in sale.items
            ],
            created_at=sale.created_at
        )


    async def get_by_shop(self, shop_id: int) -> SaleList:

        sales = await self.sale_repository.get_shop_sales(shop_id)
        
        return SaleList(
            count=len(sales),
            items=[SaleView.model_validate(sale) for sale in sales]
        )

    async def get_all(self) -> SaleList:

        sales = await self.sale_repository.get_all(
            options=[
                selectinload(Sale.shop),
                selectinload(Sale.user)
            ]
        )

        return SaleList(
            count=len(sales),
            items=[SaleView.model_validate(sale) for sale in sales]
        )

