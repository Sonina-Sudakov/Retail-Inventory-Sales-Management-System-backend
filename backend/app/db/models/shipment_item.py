from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class ShipmentItem(Base):
    __tablename__ = 'shipment_items'

    shipment_id: Mapped[int] = mapped_column(
        ForeignKey('shipments.id'),
        primary_key=True
    )

    shipment: Mapped['Shipment'] = relationship(
        back_populates='items',
        lazy='raise'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        lazy='raise'
    )

    quantity: Mapped[int] = mapped_column(
        CheckConstraint('quantity >= 0'),
        nullable=False
    )
