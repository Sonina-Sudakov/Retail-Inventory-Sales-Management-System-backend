from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import get_shop_service
from app.schemas.shop import ShopCreate, ShopList, ShopUpdate, ShopView
from app.services.shop import ShopService

router = APIRouter(prefix='/shops')


@router.get("/all", response_model=ShopList)
async def get_all_shops(
    shop_service: ShopService = Depends(get_shop_service)
):

    return await shop_service.get_all()


@router.get("/{id}", response_model=ShopView)
async def get_shop_by_id(
    id: int,
    shop_service: ShopService = Depends(get_shop_service)
):

    return await shop_service.get_by_id(id)


@router.put("/", response_model=ShopView)
async def update_shop(
    schema: ShopUpdate,
    shop_service: ShopService = Depends(get_shop_service)
):

    return await shop_service.update(schema)


@router.delete("/{id}")
async def delete_shop_by_id(
    id: int,
    shop_service: ShopService = Depends(get_shop_service)
):

    await shop_service.delete(id)

    return JSONResponse(content={'message' : 'Shop is succesfully deleted'}, status_code=200)


@router.post("/", response_model=ShopView)
async def create_shop(
    schema: ShopCreate,
    shop_service: ShopService = Depends(get_shop_service)
):

    return await shop_service.create_shop(schema)
