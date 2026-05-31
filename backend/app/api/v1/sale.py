from fastapi import APIRouter, Depends

from app.api.dependencies import get_sale_service
from app.schemas.sale import SaleCreate, SaleDetailedView, SaleList, SaleView
from app.services import SaleService

router = APIRouter(prefix='/sales')


@router.get('/all', response_model=SaleList)
async def get_all_sales(
    sale_service: SaleService = Depends(get_sale_service)
):

    return await sale_service.get_all()


@router.get('/', response_model=SaleDetailedView)
async def get_sale_by_id(
    id: int,
    sale_service: SaleService = Depends(get_sale_service)
):

    return await sale_service.get_by_id(id)


@router.get('/shop/{id}', response_model=SaleList)
async def get_sale_by_shop_id(
    id: int,
    sale_service: SaleService = Depends(get_sale_service)
):

    return await sale_service.get_by_shop(id)


@router.post('/', response_model=SaleView)
async def create_sale(
    sale: SaleCreate,
    sale_service: SaleService = Depends(get_sale_service)
):

    return await sale_service.create_sale(sale)
