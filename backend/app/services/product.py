from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.db.repositories.product import ProductRepository
from app.schemas.product import (ProductCreate, ProductList, ProductUpdate,
                                 ProductView)
from app.services.exceptions import (ProductAlreadyExistsError,
                                     ProductNotFoundError)


class ProductService:
    def __init__(self, session: AsyncSession, product_repository: ProductRepository):

        self.session = session
        self.product_repository = product_repository


    async def create_product(self, schema: ProductCreate) -> ProductView:

        product = await self.product_repository.get_by_name(schema.name) 
        if product is not None:
            raise ProductAlreadyExistsError(schema.name)

        product = Product(
            name=schema.name,
            unit=schema.unit,
            origin=schema.origin,
            type_=schema.type_,
            price=schema.price
        )

        async with self.session.begin():
            product = await self.product_repository.save(product)

        return ProductView.model_validate(product)


    async def get_by_id(self, id: int) -> ProductView:

        product = await self.product_repository.get_by_id(id)
        
        if product is None:
            raise ProductNotFoundError(id)

        return ProductView.model_validate(product)


    async def get_all(self) -> ProductList:

        products = await self.product_repository.get_all()

        return ProductList(
            count=len(products),
            items=[ProductView.model_validate(product) for product in products]
        )


    async def delete(self, id: int) -> None:
        
        product = await self.product_repository.get_by_id(id)
        
        if product is None:
            raise ProductNotFoundError(id)
    
        async with self.session.begin():
            await self.product_repository.delete(product)

    
    async def update(self, schema: ProductUpdate) -> ProductView:
        
        product = await self.product_repository.get_by_id(schema.id)
        if product is None:
            raise ProductNotFoundError(schema.id)
        
        existing_product = await self.product_repository.get_by_name(schema.name)
        if existing_product is not None and existing_product.id != schema.id:
            raise ProductAlreadyExistsError(schema.name)

        product.name=schema.name
        product.unit=schema.unit
        product.origin=schema.origin
        product.type_=schema.type_
        product.price=schema.price

        async with self.session.begin():
            product = await self.product_repository.save(product)

        return ProductView.model_validate(product)

