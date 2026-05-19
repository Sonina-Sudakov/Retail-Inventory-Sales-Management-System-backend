from decimal import Decimal

from base import Base
from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SaleItem(Base):
    __tablename__ = 'saleItems'    

    sale_id: Mapped[int] = mapped_column(
        ForeignKey('sales.id'),
        primary_key=True
    )

    sale: Mapped['Sale'] = relationship(
        back_populates='sale,
        lazy='raise'_items'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        lazy='raise'
    )

    quantity: Mapped[int] = mapped_column(
        CheckConstraint("quantity >= 0"),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        CheckConstraint("price >= 0"),
        Numeric(precision=10, scale=2),
        nullable=False
    )

