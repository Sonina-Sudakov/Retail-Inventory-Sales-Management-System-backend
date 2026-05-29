from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class SaleItem(Base):
    __tablename__ = 'saleItems'    

    sale_id: Mapped[int] = mapped_column(
        ForeignKey('sales.id'),
        primary_key=True
    )

    sale: Mapped['Sale'] = relationship(
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
        CheckConstraint("quantity >= 0"),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        CheckConstraint("price >= 0"),
        nullable=False
    )
