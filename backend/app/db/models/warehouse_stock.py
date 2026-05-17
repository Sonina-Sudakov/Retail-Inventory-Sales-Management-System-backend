from datetime import datetime

from base import Base
from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class WarehouseStock(Base):
    __tablename__ = 'warehouseStocks'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    cell_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey('products.id'),
        nullable=True
    )

    product: Mapped['Product | None'] = relationship(
        back_populates='warehouse_stocks'
    )

    quantity: Mapped[int] = mapped_column(
        CheckConstraint('quantity >= 0'),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
