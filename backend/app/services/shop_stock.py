from app.db.models.shop_stock import ShopStock
from app.db.repositories.product import ProductRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.shop_stock import ShopStockRepository
from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.shop_stock import (ProductInShopsView, ShopStockCreate,
                                    ShopStockList, ShopStockView,
                                    ShopStockWithProductView,
                                    ShopStockWithShopView,
                                    UpdateShopStockMinQuantity,
                                    UpdateShopStockQuantity)
from app.services.exceptions import (InsufficientShopStockError,
                                     InvalidMinQuantityError,
                                     InvalidQuantityError,
                                     ProductNotFoundError, ShopNotFoundError,
                                     ShopStockNotFoundError)


class ShopStockService:

    def __init__(
        self,
        shop_repository: ShopRepository,
        product_repository: ProductRepository,
        shop_stock_repository: ShopStockRepository
    ):

        self.shop_repository = shop_repository
        self.product_repository = product_repository
        self.shop_stock_repository = shop_stock_repository


    async def create_stock(
        self,
        schema: ShopStockCreate
    ) -> ShopStockView:

        await self.check_shop_and_product_existance_(schema.shop_id, schema.product_id)

        if schema.min_quantity < 0:
            raise InvalidMinQuantityError(schema.min_quantity)

        if schema.quantity < 0:
            raise InvalidQuantityError(schema.quantity)

        model = ShopStock(
            product_id=schema.product_id,
            shop_id=schema.shop_id,
            quantity=schema.quantity,
            min_quantity=schema.min_quantity
        )

        await self.shop_stock_repository.save(model)

        return ShopStockView.model_validate(
            await self.load_stock_(schema.shop_id, schema.product_id)
        )


    async def add_stock(
        self,
        schema: UpdateShopStockQuantity
    ) -> ShopStockView:

        # TODO
        # Remove try-except as main business logic

        try:
            model = await self.load_stock_(schema.shop_id, schema.product_id)

            return await self.increase_stock_quantity(schema)
        except ShopStockNotFoundError:
            return await self.create_stock(
                ShopStockCreate(
                    shop_id=schema.shop_id,
                    product_id=schema.product_id,
                    min_quantity=0,
                    quantity=schema.change
                )
            )


    async def increase_stock_quantity(
        self,
        schema: UpdateShopStockQuantity
        ) -> ShopStockView:

        await self.check_shop_and_product_existance_(schema.shop_id, schema.product_id)

        model = await self.load_stock_(schema.shop_id, schema.product_id)

        model.quantity += schema.change

        model = await self.shop_stock_repository.save(model)

        return ShopStockView.model_validate(model)


    async def decrease_stock_quantity(
        self,
        schema: UpdateShopStockQuantity
        ) -> ShopStockView:

        await self.check_shop_and_product_existance_(schema.shop_id, schema.product_id)

        model = await self.load_stock_(schema.shop_id, schema.product_id)

        if model.quantity - schema.change < 0:
            raise InsufficientShopStockError(schema.shop_id, schema.product_id, model.quantity, schema.change)

        model.quantity -= schema.change

        model = await self.shop_stock_repository.save(model)

        return ShopStockView.model_validate(model)


    async def update_stock_min_quantity(
        self,
        schema: UpdateShopStockMinQuantity
    ) -> ShopStockView:

        await self.check_shop_and_product_existance_(schema.shop_id, schema.product_id)

        model = await self.load_stock_(schema.shop_id, schema.product_id)

        if schema.min_quantity < 0:
            raise InvalidMinQuantityError(schema.min_quantity)
        
        model.min_quantity = schema.min_quantity

        model = await self.shop_stock_repository.save(model)

        return ShopStockView.model_validate(model)


    async def get_shop_stocks(
        self,
        shop_id: int
    ) -> ShopStockList:

        shop = await self.shop_repository.get_by_id(shop_id)

        if not shop:
            raise ShopNotFoundError(shop_id)

        models = await self.shop_stock_repository.get_shop_stocks(shop_id)

        return ShopStockList(
            shop=ShopView.model_validate(shop),
            count=len(models),
            items=[
                ShopStockWithProductView.model_validate(stock)
                for stock in models
            ]
        )


    async def get_product_in_shops(
        self,
        product_id: int
    ) -> ProductInShopsView:

        product = await self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(product_id)

        models = await self.shop_stock_repository.get_product_in_shops(product_id)

        return ProductInShopsView(
            product=ProductView.model_validate(product),
            count=len(models),
            items=[
                ShopStockWithShopView.model_validate(stock)
                for stock in models
            ]
        )


    async def get_full_stock_info(
        self,
        shop_id: int,
        product_id: int
    ) -> ShopStockView:

        await self.check_shop_and_product_existance_(shop_id, product_id)

        return ShopStockView.model_validate(await self.load_stock_(shop_id, product_id))


    async def delete_stock(
        self,
        shop_id: int,
        product_id: int
    ) -> None:

        await self.check_shop_and_product_existance_(shop_id, product_id)

        model = await self.load_stock_(shop_id, product_id)

        await self.shop_stock_repository.delete(model)


    async def check_shop_and_product_existance_(
        self,
        shop_id: int,
        product_id: int
    ) -> None:

        existing_shop = await self.shop_repository.get_by_id(shop_id)
        if not existing_shop:
            raise ShopNotFoundError(shop_id)

        existing_product = await self.product_repository.get_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundError(product_id)


    async def load_stock_(
        self,
        shop_id: int,
        product_id: int
    ) -> ShopStock:

        model = await self.shop_stock_repository.get_shop_stock(shop_id, product_id)

        if not model:
            raise ShopStockNotFoundError(shop_id, product_id)

        return model
