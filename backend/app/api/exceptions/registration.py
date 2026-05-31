from fastapi import FastAPI

from app.api.exceptions.handlers import (empty_order_handler,
                                         insufficient_shop_stock_error_handler,
                                         invalid_min_quantity_error_handler,
                                         invalid_quantity_error_handler,
                                         order_is_not_pending_handler,
                                         order_not_found_handler,
                                         passwords_mismatch_handler,
                                         product_already_exists_handler,
                                         product_not_found_handler,
                                         shop_already_exists_handler,
                                         shop_not_found_handler,
                                         shop_stock_not_found_handler,
                                         user_already_exists_handler,
                                         user_not_found_handler)
from app.services.exceptions import (EmptyOrderError,
                                     InsufficientShopStockError,
                                     InvalidMinQuantityError,
                                     InvalidQuantityError,
                                     OrderIsNotPendingError,
                                     OrderNotFoundError,
                                     ProductAlreadyExistsError,
                                     ProductNotFoundError,
                                     ShopAlreadyExistsError, ShopNotFoundError,
                                     ShopStockNotFoundError,
                                     UserAlreadyExistsError, UserNotFoundError,
                                     UserPasswordsMismatchError)


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
        UserPasswordsMismatchError,
        passwords_mismatch_handler
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
