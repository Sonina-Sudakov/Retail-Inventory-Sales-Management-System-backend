from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        id: int
    ) -> ModelType | None:

        return await self.session.get(
            self.model,
            id
        )


    async def get_all(
        self
    ) -> list[ModelType]:

        stmt = select(self.model)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def create(
        self,
        entity: ModelType
    ) -> ModelType:

        self.session.add(entity)

        await self.session.commit()

        await self.session.refresh(entity)

        return entity


    async def delete(
        self,
        entity: ModelType
    ) -> None:
        
        await self.session.delete(entity)

        await self.session.commit()
