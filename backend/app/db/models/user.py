from datetime import datetime

from sqlalchemy import CheckConstraint, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.models.base import Base
from app.db.models.shop import Shop
from app.enums import UserRole


class User(Base):
    __tablename__ = 'users'

    __table_args__ = (
        CheckConstraint(
            f"(role = '{UserRole.SHOPKEEPER.value}' AND works_in_shop_id IS NOT NULL) OR "
            f"(role = '{UserRole.STOREKEEPER.value}' AND works_in_shop_id IS NULL)",
            name="check_shopkeeper_has_shop",
        ),
    )

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

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False
    )

    works_in_shop_id: Mapped[int | None] = mapped_column(
        ForeignKey('shops.id'),
        nullable=True
    )

    works_in_shop: Mapped['Shop | None'] = relationship(
        lazy='raise'
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


    @validates("works_in_shop_id", "role")
    def validate_user_role_and_shop(self, key, value):

        role = value if key == "role" else self.role
        shop_id = value if key == "works_in_shop_id" else self.works_in_shop_id

        if role == UserRole.SHOPKEEPER and shop_id is None:
            raise ValueError("ShopKeeper must have works_in_shop_id populated.")

        if role == UserRole.STOREKEEPER and shop_id is not None:
            raise ValueError("StoreKeeper cannot have a works_in_shop_id.")

        return value
