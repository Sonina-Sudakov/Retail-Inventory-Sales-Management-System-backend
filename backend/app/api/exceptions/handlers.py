from fastapi import Request
from fastapi.responses import JSONResponse

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

# ---[[ USER ]]--- #

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


# ---[[ SHOP STOCKS ]]--- #


async def shop_stock_not_found_handler(
    request: Request,
    exc: ShopStockNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Shop stock with shop_id = {exc.shop_id} and product_id = {exc.product_id} doesn't exist"
        }
    )


async def insufficient_shop_stock_error_handler(
    request: Request,
    exc: InsufficientShopStockError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Not enough quantity in shop stock with shop_id = {exc.shop_id} and product_id = {exc.product_id} to decrease it for {exc.change}"
        }
    )


async def invalid_quantity_error_handler(
    request: Request,
    exc: InvalidQuantityError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Quantity value must be greater or equal than zero (received {exc.quantity})"
        }
    )


async def invalid_min_quantity_error_handler(
    request: Request,
    exc: InvalidMinQuantityError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Minimal quantity value must be greater or equal than zero (received {exc.min_quantity})"
        }
    )


# ---[[ ORDER ]] --- #


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


# ---[[ SALE ]]--- #



async def sale_not_found_handler(
    request: Request,
    exc: SaleNotFoundError 
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Sale with id = {exc.sale_id} doesn't exist"
        }
    )


async def empty_sale_handler(
    request: Request,
    exc: EmptySaleError
):
    return JSONResponse(
        status_code=400,
        content={
            "message":
                f"Sale must contain at least one item"
        }
    )


# ---[[ WAREHOUSE ]]--- #


async def warehouse_stock_already_exists_handler(
    request: Request,
    exc: WarehouseStockAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Warehouse stock with cell code = {exc.cell_code} already exists"
        }
    )


async def warehouse_stock_not_found_handler(
    request: Request,
    exc: WarehouseStockNotFoundError 
):
    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Warehouse stock with id = {exc.id} doesn't exist"
        }
    )


async def insufficient_warehouse_stock_handler(
    request: Request,
    exc: InsufficientWarehouseStockError 
):
    return JSONResponse(
        status_code=422,
        content={
            "message":
                f"Not enough quantity ({exc.quantity}) in warehouse stock with id = {exc.id} to decrease it for {exc.change}"
        }
    )


async def invalid_change_value_handler(
    request: Request,
    exc: InvalidChangeValueError
):
    return JSONResponse(
        status_code=422,
        content={
            "message":
                f"Change value must be positive number (received {exc.change})"
        }
    )


async def duplicate_cell_code_handler(
    request: Request,
    exc: DuplicateCellCodeError
):
    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Cell with cell code = {exc.cell_code} already exists"
        }
    )
