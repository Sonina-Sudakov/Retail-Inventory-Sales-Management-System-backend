from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    fullname: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    hash_password: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(15),
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

    sales: Mapped[list['Sale']] = relationship(
        back_populates='user'
    )
