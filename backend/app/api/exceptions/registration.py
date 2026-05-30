from fastapi import FastAPI

from app.api.exceptions.handlers import (passwords_mismatch_handler,
                                         product_already_exists_handler,
                                         product_not_found_handler,
                                         shop_already_exists_handler,
                                         shop_not_found_handler,
                                         user_already_exists_handler,
                                         user_not_found_handler)
from app.services.exceptions import (ProductAlreadyExistsError,
                                     ProductNotFoundError,
                                     ShopAlreadyExistsError, ShopNotFoundError,
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
