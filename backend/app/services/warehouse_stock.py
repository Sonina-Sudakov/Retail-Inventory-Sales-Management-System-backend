from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.db.models.warehouse_stock import WarehouseStock
from app.db.repositories.product import ProductRepository
from app.db.repositories.warehouse_stock import WarehouseStockRepository
from app.schemas.product import ProductView
from app.schemas.warehouse_stock import (ChangeWarehouseStockCellCode,
                                         ProductInWarehouseList,
                                         StoreProductInStock,
                                         WarehouseStockCreate,
                                         WarehouseStockList,
                                         WarehouseStockView,
                                         WarehouseStockViewWithoutProduct,
                                         WarehouseSwapProductsView)
from app.services.exceptions import (DuplicateCellCodeError,
                                     InsufficientWarehouseStockError,
                                     InvalidChangeValueError,
                                     InvalidQuantityError,
                                     ProductNotFoundError,
                                     WarehouseStockAlreadyExistsError,
                                     WarehouseStockNotFoundError)


class WarehouseStockService:

    def __init__(
        self,
        warehouse_stock_repository: WarehouseStockRepository,
        product_repository: ProductRepository
    ):

        self.warehouse_stock_repository = warehouse_stock_repository
        self.product_repository = product_repository


    async def create_stock(
        self,
        schema: WarehouseStockCreate
    ) -> WarehouseStockView:

        if schema.quantity < 0:
            raise InvalidQuantityError(schema.quantity)

        if schema.product_id is not None:
            product = await self.product_repository.get_by_id(schema.product_id)

            if not product:
                raise ProductNotFoundError(schema.product_id)

        model = await self.warehouse_stock_repository.get_stock_by_cell_code(schema.cell_code)

        if model:
            raise WarehouseStockAlreadyExistsError(schema.cell_code)

        model = WarehouseStock(
            cell_code=schema.cell_code,
            product_id=schema.product_id,
            quantity=schema.quantity
        )

        model = await self.warehouse_stock_repository.save(model)

        model = await self.warehouse_stock_repository.get_stock_by_cell_code(schema.cell_code)

        return WarehouseStockView.model_validate(model)


    async def get_all_stocks(
        self
    ) -> WarehouseStockList:
        
        models = await self.warehouse_stock_repository.get_all(
            options=[selectinload(WarehouseStock.product)]
        )

        return WarehouseStockList(
            count=len(models),
            items=[
                WarehouseStockView.model_validate(stock)
                for stock in models
            ]
        )


    async def get_stock_by_id(
        self,
        id: int
    ) -> WarehouseStockView:

        return WarehouseStockView.model_validate(await self.load_stock_(id))


    async def get_stocks_by_product_id(
        self,
        product_id: int
    ) -> ProductInWarehouseList:

        product = await self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(product_id)

        models = await self.warehouse_stock_repository.get_product_in_warehouse(product_id)

        total_qty = sum(model.quantity for model in models)

        return ProductInWarehouseList(
            product=ProductView.model_validate(product),
            count=len(models),
            total_quantity=total_qty,
            items=[
                WarehouseStockViewWithoutProduct.model_validate(stock)
                for stock in models
            ]
        )


    async def increase_stock_quantity(
        self,
        id: int,
        change: int
    ) -> WarehouseStockView:

        if change < 0:
            raise InvalidChangeValueError(change)

        model = await self.load_stock_(id)

        model.quantity += change

        await self.warehouse_stock_repository.save(model)

        return WarehouseStockView.model_validate(model)


    async def decrease_stock_quantity(
        self,
        id: int,
        change: int
    ) -> WarehouseStockView:

        if change < 0:
            raise InvalidChangeValueError(change)

        model = await self.load_stock_(id)

        if model.quantity - change < 0:
            raise InsufficientWarehouseStockError(id, model.quantity, change)

        model.quantity -= change

        await self.warehouse_stock_repository.save(model)

        return WarehouseStockView.model_validate(model)


    async def change_stock_cell_code(
        self,
        schema: ChangeWarehouseStockCellCode
    ) -> WarehouseStockView:

        model = await self.load_stock_(schema.id)

        model.cell_code = schema.cell_code

        try:
            model = await self.warehouse_stock_repository.save(model)
        except IntegrityError:
            raise DuplicateCellCodeError(schema.cell_code)

        return WarehouseStockView.model_validate(model)


    async def swap_products(
        self,
        first_id: int,
        second_id: int
    ) -> WarehouseSwapProductsView:

        first_model = await self.load_stock_(first_id)

        second_model = await self.load_stock_(second_id)

        first_model.product_id, second_model.product_id \
            = second_model.product_id, first_model.product_id
        first_model.quantity, second_model.quantity = second_model.quantity, first_model.quantity

        first_model = await self.warehouse_stock_repository.save(first_model)
        second_model = await self.warehouse_stock_repository.save(second_model)

        return WarehouseSwapProductsView(
            first_stock=WarehouseStockView.model_validate(first_model),
            second_stock=WarehouseStockView.model_validate(second_model),
        )


    async def clear_stock(
        self,
        id: int
    ) -> WarehouseStockView:

        model = await self.load_stock_(id)

        model.product_id = None
        model.quantity = 0

        model = await self.warehouse_stock_repository.save(model)

        return WarehouseStockView.model_validate(model)

    
    async def store_product_in_stock(
        self,
        schema: StoreProductInStock
    ) -> WarehouseStockView:

        if schema.quantity < 0:
            raise InvalidQuantityError(schema.quantity)

        product = await self.product_repository.get_by_id(schema.product_id)

        if not product:
            raise ProductNotFoundError(schema.product_id)

        model = await self.load_stock_(schema.stock_id)

        model.product_id = schema.product_id
        model.quantity = schema.quantity

        model = await self.warehouse_stock_repository.save(model)

        return WarehouseStockView.model_validate(model)


    async def delete_stock(
        self,
        id: int
    ) -> None:

        model = await self.load_stock_(id)

        await self.warehouse_stock_repository.delete(model)



    async def load_stock_(
        self,
        id: int
    ) -> WarehouseStock:

        model = await self.warehouse_stock_repository.get_by_id(
            id,
            options=[selectinload(WarehouseStock.product)]
        )

        if not model:
            raise WarehouseStockNotFoundError(id)

        return model
