from decimal import Decimal

from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class ShipmentItem(Base):
    __tablename__ = 'shipmentItems'    

    shipment_id: Mapped[int] = mapped_column(
        ForeignKey('shipments.id'),
        primary_key=True
    )

    shipment: Mapped['Shipment'] = relationship(
        back_populates='shipment_items'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        back_populates='shipment_items'
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )
