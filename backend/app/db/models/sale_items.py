from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class SaleItems(Base):
    __tablename__ = 'saleItems'    

    sale_id: Mapped[int] = mapped_column(
        ForeignKey('sales.id'),
        primary_key=True
    )

    sale: Mapped['Shop'] = relationship(
        back_populates='sale_items'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        back_populates='sale_items'
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

