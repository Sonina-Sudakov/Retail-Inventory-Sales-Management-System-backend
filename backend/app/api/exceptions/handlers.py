from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (EmptyOrderError, OrderIsNotPendingError,
                                     OrderNotFoundError,
                                     ProductAlreadyExistsError,
                                     ProductNotFoundError,
                                     ShopAlreadyExistsError, ShopNotFoundError,
                                     UserAlreadyExistsError, UserNotFoundError,
                                     UserPasswordsMismatchError)

# ---[[ USER ]]---

async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"User with id = {exc.user_id} doesn't exist"
        }
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"User with username = {exc.username} already exists"
        }
    )


async def passwords_mismatch_handler(
    request: Request,
    exc: UserPasswordsMismatchError
):

    return JSONResponse(
        status_code=422,
        content={
            "message":
                f"Wrong old password for user {exc.username}"
        }
    )


async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Product with id = {exc.product_id} doesn't exist"
        }
    )


async def product_already_exists_handler(
    request: Request,
    exc: ProductAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Product with name = {exc.name} already exists"
        }
    )


async def shop_not_found_handler(
    request: Request,
    exc: ShopNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Shop with id = {exc.shop_id} doesn't exist"
        }
    )


async def shop_already_exists_handler(
    request: Request,
    exc: ShopAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Shop with the same data (phone number = {exc.phone_number} or email = {exc.email}) already exists"
        }
    )


# ---[[ ORDER ]] ---


async def order_not_found_handler(
    request: Request,
    exc: OrderNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Order with id = {exc.order_id} doesn't exist"
        }
    )


async def order_is_not_pending_handler(
    request: Request,
    exc: OrderIsNotPendingError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Order with id = {exc.order_id} isn't pending"
        }
    )


async def empty_order_handler(
    request: Request,
    exc: EmptyOrderError
):
    return JSONResponse(
        status_code=400,
        content={
            "message":
                f"Order must contain at least one item"
        }
    )

