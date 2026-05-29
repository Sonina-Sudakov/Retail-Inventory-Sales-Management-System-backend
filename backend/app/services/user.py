from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.schemas.user import (UserCreate, UserList, UserUpdateFullname,
                              UserUpdatePassword, UserView)
from app.services.exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):

        self.session = session
        self.user_repository = user_repository
        

    async def create(self, schema: UserCreate) -> UserView:

        user = await self.user_repository.get_by_username(schema.username)
        if user is not None:
            raise UserAlreadyExistsError(schema.username)

        user = User(
            username=schema.username,
            fullname=schema.fullname,
            hash_password=schema.password, # TODO add bcrypt
            role=schema.role
        )

        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserView.model_validate(user)

        
    async def get_by_id(self, id: int) -> UserView:

        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)

        return UserView.model_validate(user)


    async def get_all(self) -> UserList:

        users = await self.user_repository.get_all()

        return UserList(
            count=len(users),
            items=[UserView.model_validate(user) for user in users]
        )


    async def delete(self, id: int) -> None:
        
        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)
    
        async with self.session.begin():
            await self.user_repository.delete(user)


    async def change_fullname(self, schema: UserUpdateFullname) -> UserView:

        user = await self.user_repository.get_by_id(schema.id)
        
        if user is None:
            raise UserNotFoundError(schema.id)

        user.fullname = schema.fullname
        
        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserView.model_validate(user)


    async def change_password(self, schema: UserUpdatePassword) -> UserView:

        user = await self.user_repository.get_by_id(schema.id)
        
        if user is None:
            raise UserNotFoundError(schema.id)

        user.hash_password = schema.password # TODO add bcrypt
        
        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserView.model_validate(user)
