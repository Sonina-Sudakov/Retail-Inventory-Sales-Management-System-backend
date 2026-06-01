from sqlalchemy.orm import selectinload

import app.core.secutiry as security
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.schemas.user import (UserCreate, UserList, UserUpdateFullname,
                              UserUpdatePassword, UserUpdateWorkplace,
                              UserView)
from app.services.exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    def __init__(self, user_repository: UserRepository):

        self.user_repository = user_repository
        

    async def create(self, schema: UserCreate) -> UserView:

        user = await self.user_repository.get_by_username(schema.username)

        if user is not None:
            raise UserAlreadyExistsError(schema.username)

        hash_password = security.hash_password(schema.password)

        user = User(
            username=schema.username,
            fullname=schema.fullname,
            hash_password=hash_password,
            role=schema.role
        )

        user = await self.user_repository.save(user)

        user = await self.load_user_(user.id)

        return UserView.model_validate(user)

        
    async def get_by_id(self, id: int) -> UserView:

        user = await self.load_user_(id)

        return UserView.model_validate(user)


    async def get_all(self) -> UserList:

        users = await self.user_repository.get_all(
            options=[selectinload(User.works_in_shop)]
        )

        return UserList(
            count=len(users),
            items=[UserView.model_validate(user) for user in users]
        )


    async def delete(self, id: int) -> None:
        
        user = await self.load_user_(id)
    
        await self.user_repository.delete(user)


    async def change_fullname(self, schema: UserUpdateFullname) -> UserView:

        user = await self.load_user_(schema.id)
        
        user.fullname = schema.new_fullname
        
        user = await self.user_repository.save(user)

        return UserView.model_validate(user)


    async def change_password(self, schema: UserUpdatePassword) -> UserView:

        user = await self.load_user_(schema.id)
        
        user.hash_password = security.hash_password(schema.new_password)
        
        user = await self.user_repository.save(user)

        return UserView.model_validate(user)


    async def update_workplace(
        self,
        schema: UserUpdateWorkplace
    ) -> UserView:

        model = await self.load_user_(schema.id)

        model.works_in_shop_id = schema.shop_id

        await self.user_repository.save(model)

        return UserView.model_validate(model)


    async def load_user_(
        self,
        id: int
    ) -> User:

        user = await self.user_repository.get_by_id(
            id,
            options=[selectinload(User.works_in_shop)]
        )

        if not user:
            raise UserNotFoundError(id)

        return user
