from typing import Generic, TypeVar

from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

ModelType = TypeVar('ModelType')


class BaseRepository(
    Generic[ModelType]
):
    def __init__(
        self,
        model: type[ModelType],
        session: AsyncSession
    ):

        self.model = model
        self.session = session


    async def get_by_id(
        self,
        id: int,
        options: Sequence[ORMOption] | None = None
    ) -> ModelType | None:

        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_all(
        self,
        options: Sequence[ORMOption] | None = None
    ) -> list[ModelType]:

        stmt = select(self.model)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def save(
        self,
        entity: ModelType
    ) -> ModelType:

        self.session.add(entity)

        await self.session.flush()

        await self.session.refresh(entity)

        return entity


    async def delete(
        self,
        entity: ModelType
    ) -> None:
        
        await self.session.delete(entity)

        await self.session.flush()
