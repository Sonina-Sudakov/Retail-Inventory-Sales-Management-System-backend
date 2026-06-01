from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_product_service
from app.schemas.product import (ProductCreate, ProductList, ProductUpdate,
                                 ProductView)
from app.services.product import ProductService

router = APIRouter(prefix='/products')


@router.post('/', response_model=ProductView)
async def create_product(
    product: ProductCreate,
    product_service: ProductService = Depends(get_product_service)
): 
    
    return await product_service.create_product(product)


@router.get('/', response_model=ProductView)
async def get_product_by_id(
    id: int,
    product_service: ProductService = Depends(get_product_service)
):

    return await product_service.get_by_id(id)


@router.get('/all', response_model=ProductList)
async def get_all_products(
    product_service: ProductService = Depends(get_product_service)
):

    return await product_service.get_all()


@router.delete('/')
async def delete_product_by_id(
    id: int,
    product_service: ProductService = Depends(get_product_service)
):
    
    await product_service.delete(id)

    return Response(status_code=204)


@router.put('/', response_model=ProductView)
async def update_product(
    product: ProductUpdate,
    product_service: ProductService = Depends(get_product_service)
):
    
    return await product_service.update(product)
