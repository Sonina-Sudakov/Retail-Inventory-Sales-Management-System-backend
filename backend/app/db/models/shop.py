from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(60),
        unique=True,
        nullable=False
    )

    adress: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    contactFace: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    phoneNumber: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(60),
        unique=True,
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
