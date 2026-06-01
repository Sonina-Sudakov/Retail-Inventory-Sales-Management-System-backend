from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'),
        primary_key=True
    )

    order: Mapped['Order'] = relationship(
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
        nullable=False
    )
