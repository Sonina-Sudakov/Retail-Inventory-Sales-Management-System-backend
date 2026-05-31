from fastapi import FastAPI

from app.api.exceptions.handlers import (
    duplicate_cell_code_handler, empty_order_handler, empty_sale_handler,
    insufficient_shop_stock_error_handler,
    insufficient_warehouse_stock_handler, invalid_change_value_handler,
    invalid_min_quantity_error_handler, invalid_quantity_error_handler,
    order_is_not_pending_handler, order_not_found_handler,
    product_already_exists_handler, product_not_found_handler,
    sale_not_found_handler, shop_already_exists_handler,
    shop_not_found_handler, shop_stock_not_found_handler,
    user_already_exists_handler, user_not_found_handler,
    warehouse_stock_already_exists_handler, warehouse_stock_not_found_handler)
from app.services.exceptions import (DuplicateCellCodeError, EmptyOrderError,
                                     EmptySaleError,
                                     InsufficientShopStockError,
                                     InsufficientWarehouseStockError,
                                     InvalidChangeValueError,
                                     InvalidMinQuantityError,
                                     InvalidQuantityError,
                                     OrderIsNotPendingError,
                                     OrderNotFoundError,
                                     ProductAlreadyExistsError,
                                     ProductNotFoundError, SaleNotFoundError,
                                     ShopAlreadyExistsError, ShopNotFoundError,
                                     ShopStockNotFoundError,
                                     UserAlreadyExistsError, UserNotFoundError,
                                     WarehouseStockAlreadyExistsError,
                                     WarehouseStockNotFoundError)


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        UserNotFoundError,
        user_not_found_handler
    )

    app.add_exception_handler(
        UserAlreadyExistsError,
        user_already_exists_handler
    )

    app.add_exception_handler(
        ProductNotFoundError,
        product_not_found_handler
    )

    app.add_exception_handler(
        ProductAlreadyExistsError,
        product_already_exists_handler
    )

    app.add_exception_handler(
        ShopNotFoundError,
        shop_not_found_handler
    )

    app.add_exception_handler(
        ShopAlreadyExistsError,
        shop_already_exists_handler
    )

    app.add_exception_handler(
        OrderNotFoundError,
        order_not_found_handler
    )

    app.add_exception_handler(
        OrderIsNotPendingError,
        order_is_not_pending_handler
    )

    app.add_exception_handler(
        EmptyOrderError,
        empty_order_handler
    )

    app.add_exception_handler(
        ShopStockNotFoundError,
        shop_stock_not_found_handler
    )

    app.add_exception_handler(
        InsufficientShopStockError,
        insufficient_shop_stock_error_handler 
    )

    app.add_exception_handler(
        InvalidQuantityError,
        invalid_quantity_error_handler 
    )

    app.add_exception_handler(
        InvalidMinQuantityError,
        invalid_min_quantity_error_handler
    )

    app.add_exception_handler(
        SaleNotFoundError,
        sale_not_found_handler 
    )

    app.add_exception_handler(
        EmptySaleError,
        empty_sale_handler
    )

    app.add_exception_handler(
        WarehouseStockAlreadyExistsError,
        warehouse_stock_already_exists_handler
    )

    app.add_exception_handler(
        WarehouseStockNotFoundError,
        warehouse_stock_not_found_handler
    )

    app.add_exception_handler(
        InsufficientWarehouseStockError,
        insufficient_warehouse_stock_handler
    )

    app.add_exception_handler(
        InvalidChangeValueError,
        invalid_change_value_handler
    )

    app.add_exception_handler(
        DuplicateCellCodeError,
        duplicate_cell_code_handler
    )
