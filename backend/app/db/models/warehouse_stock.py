from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class WarehouseStock(Base):
    __tablename__ = 'warehouse_stocks'

    __table_args__ = (
        CheckConstraint('quantity >= 0'),
    )

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
        lazy='raise'
    )

    quantity: Mapped[int] = mapped_column(
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
