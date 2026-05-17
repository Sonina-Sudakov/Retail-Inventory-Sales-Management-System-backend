from decimal import Decimal

from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class OrderItems(Base):
    __tablename__ = 'saleItems'    

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'),
        primary_key=True
    )

    order: Mapped['Order'] = relationship(
        back_populates='order_items'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        back_populates='order_items'
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

