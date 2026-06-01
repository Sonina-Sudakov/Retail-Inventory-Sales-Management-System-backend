from fastapi import APIRouter, Depends, Response

from app.api.dependencies import get_shop_service, get_shop_stock_service
from app.core.auth.dependencies import get_current_user, require_role
from app.enums import UserRole
from app.schemas.shop import ShopCreate, ShopList, ShopUpdate, ShopView
from app.schemas.shop_stock import (ShopStockCreate, ShopStockList,
                                    ShopStockView, UpdateShopStockMinQuantity)
from app.services.shop import ShopService
from app.services.shop_stock import ShopStockService

router = APIRouter(prefix='/shops')


@router.get("/all", response_model=ShopList)
async def get_all_shops(
    shop_service: ShopService = Depends(get_shop_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await shop_service.get_all()


@router.get("/", response_model=ShopView)
async def get_shop_by_id(
    id: int,
    shop_service: ShopService = Depends(get_shop_service),
    user=Depends(
        get_current_user
    )
):

    return await shop_service.get_by_id(id)


@router.put("/", response_model=ShopView)
async def update_shop(
    schema: ShopUpdate,
    shop_service: ShopService = Depends(get_shop_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await shop_service.update(schema)


@router.delete("/")
async def delete_shop_by_id(
    id: int,
    shop_service: ShopService = Depends(get_shop_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    await shop_service.delete(id)

    return Response(status_code=204)


@router.post("/", response_model=ShopView)
async def create_shop(
    schema: ShopCreate,
    shop_service: ShopService = Depends(get_shop_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await shop_service.create_shop(schema)


@router.post('/stocks', response_model=ShopStockView)
async def create_shop_stock(
    schema: ShopStockCreate,
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    return await shop_stock_service.create_stock(schema)


@router.get('/stocks', response_model=ShopStockView)
async def get_shop_stock(
    shop_id: int,
    product_id: int,
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    return await shop_stock_service.get_full_stock_info(shop_id, product_id)


@router.get('/{id}/stocks', response_model=ShopStockList)
async def get_shop_stocks(
    id: int,
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    return await shop_stock_service.get_shop_stocks(id)


@router.put('/stocks', response_model=ShopStockView)
async def update_shop_stock_min_quantity(
    schema: UpdateShopStockMinQuantity,
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    return await shop_stock_service.update_stock_min_quantity(schema)


@router.delete('/stocks')
async def delete_shop_stock(
    shop_id: int,
    product_id: int,
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    await shop_stock_service.delete_stock(shop_id, product_id)

    return Response(status_code=204)
