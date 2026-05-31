from sqlalchemy.orm.strategy_options import selectinload

from app.db.models.shipment import Shipment
from app.db.models.shipment_item import ShipmentItem
from app.db.repositories.product import ProductRepository
from app.db.repositories.shipment import ShipmentRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.enums import ShipmentStatus
from app.schemas.shipment import (ShipmentCreate, ShipmentDetailedView,
                                  ShipmentList, ShipmentView)
from app.schemas.shop_stock import UpdateShopStockQuantity
from app.services.exceptions import (EmptyShipmentError, ProductNotFoundError,
                                     ShipmentAlreadyAcceptedError,
                                     ShipmentAlreadyCancelledError,
                                     ShipmentNotFoundError, ShopNotFoundError,
                                     UserNotFoundError)
from app.services.shop_stock import ShopStockService
from app.services.warehouse_stock import WarehouseStockService


class ShipmentService:
    def __init__(
            self, 
            shipment_repository: ShipmentRepository, 
            shop_repository: ShopRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository,
            warehouse_stock_service: WarehouseStockService,
            shop_stock_service: ShopStockService
        ):
        
        self.shipment_repository = shipment_repository
        self.shop_repository = shop_repository
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.warehouse_stock_service = warehouse_stock_service
        self.shop_stock_service = shop_stock_service


    async def create_shipment(self, schema: ShipmentCreate) -> ShipmentView:
      
        if not schema.items:
            raise EmptyShipmentError()
        
        if schema.to_shop_id is not None:

            shop = await self.shop_repository.get_by_id(schema.to_shop_id)

            if shop is None:
                raise ShopNotFoundError(schema.to_shop_id)

        user = await self.user_repository.get_by_id(schema.created_by_id)

        if user is None:
            raise UserNotFoundError(schema.created_by_id)

        for item in schema.items:
            product = self.product_repository.get_by_id(item.product_id)

            if not product:
                raise ProductNotFoundError(item.product_id)

            if schema.to_shop_id is not None:
                await self.warehouse_stock_service.decrease_stock_quantity(item.product_id, item.quantity)

        shipment = Shipment(
            from_location=schema.from_location,
            to_shop_id=schema.to_shop_id,
            created_by_id=schema.created_by_id,
            items=[
                ShipmentItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )

                for item in schema.items
            ]
        )

        shipment = await self.shipment_repository.save(shipment)

        if schema.to_shop_id is not None:
            await self.accept_shipment(shipment.id, shipment.created_by_id)

        return ShipmentView.model_validate(shipment)


    async def get_by_id(self, id: int) -> ShipmentDetailedView:

        shipment = await self.shipment_repository.get_by_id(
            id,
            options=[selectinload(Shipment.items)]
        )
        
        if shipment is None:
            raise ShipmentNotFoundError(id)

        return ShipmentDetailedView.model_validate(shipment)


    async def get_by_shop(self, shop_id: int) -> ShipmentList:

        shipments = await self.shipment_repository.get_shop_shipments(shop_id)
        
        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def get_by_status(self, status: ShipmentStatus) -> ShipmentList:

        shipments = await self.shipment_repository.get_shipments_by_status(status)
        
        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def get_all(self) -> ShipmentList:

        shipments = await self.shipment_repository.get_all()

        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def update_status(self, id: int, status: ShipmentStatus) -> ShipmentView:
        
        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        shipment.status = status

        shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)


    async def accept_shipment(
        self,
        id: int,
        user_id: int
    ) -> ShipmentView:

        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if shipment.status == ShipmentStatus.CANCELED:
            raise ShipmentAlreadyCancelledError(id)

        if shipment.to_shop_id is not None:
            for item in shipment.items:
                await self.shop_stock_service.increase_stock_quantity(
                    UpdateShopStockQuantity(
                        shop_id=shipment.to_shop_id,
                        product_id=item.id,
                        change=item.quantity
                    )
                )
        else:
            for item in shipment.items:
                await self.warehouse_stock_service.increase_stock_quantity(
                    item.id,
                    item.quantity
                )

        shipment.status = ShipmentStatus.ACCEPTED
        shipment.accepted_by_id = user_id

        shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)


    async def cancel_shipment(
        self,
        id: int
    ) -> ShipmentView:

        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        if shipment.status == ShipmentStatus.ACCEPTED:
            raise ShipmentAlreadyAcceptedError(id)

        shipment.status = ShipmentStatus.CANCELED

        shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)
