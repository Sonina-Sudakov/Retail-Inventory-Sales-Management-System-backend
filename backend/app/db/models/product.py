from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    origin: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    type_: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        name='type'
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
