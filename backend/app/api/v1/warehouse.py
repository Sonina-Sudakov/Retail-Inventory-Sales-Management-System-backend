from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_warehouse_stock_service
from app.schemas.warehouse_stock import (ChangeWarehouseStockCellCode,
                                         ProductInWarehouseList,
                                         StoreProductInStock,
                                         WarehouseStockCreate,
                                         WarehouseStockList,
                                         WarehouseStockView,
                                         WarehouseSwapProductsView)
from app.services.warehouse_stock import WarehouseStockService

router = APIRouter(prefix='/warehouse')


@router.post('/', response_model=WarehouseStockView)
async def create_stock(
    schema: WarehouseStockCreate,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.create_stock(schema)


@router.get('/all', response_model=WarehouseStockList)
async def get_all(
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.get_all_stocks()


@router.get('/', response_model=WarehouseStockView)
async def get_by_id(
    id: int,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.get_stock_by_id(id)


@router.get('/product', response_model=ProductInWarehouseList)
async def get_product_in_warehouse(
    id: int,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.get_stocks_by_product_id(id)


@router.put('/change_cell_code', response_model=WarehouseStockView)
async def change_stock_cell_code(
    schema: ChangeWarehouseStockCellCode,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.change_stock_cell_code(schema)


@router.put('/swap_products', response_model=WarehouseSwapProductsView)
async def swap_warehouse_products(
    first_id: int,
    second_id: int,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.swap_products(first_id, second_id)


@router.put('/clear', response_model=WarehouseStockView)
async def clear_warehouse_stock(
    id: int,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.clear_stock(id)


@router.put('/store', response_model=WarehouseStockView)
async def store_product(
    schema: StoreProductInStock,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    return await warehouse_service.store_product_in_stock(schema)


@router.delete('/')
async def delete_stock(
    id: int,
    warehouse_service: WarehouseStockService = Depends(get_warehouse_stock_service)
):

    await warehouse_service.delete_stock(id)

    return Response(status_code=204)
