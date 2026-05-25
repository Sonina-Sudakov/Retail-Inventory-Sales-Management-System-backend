from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import (UserCreateDTO, UserListDTO,
                              UserUpdateFullnameDTO, UserUpdatePasswordDTO,
                              UserViewDTO)
from app.services.exceptions import UserAlreadyExistsError, UserNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):

        self.session = session
        self.user_repository = user_repository
        

    async def create(self, schema: UserCreateDTO) -> UserViewDTO:

        if self.user_repository.get_by_username(schema.username) is not None:
            raise UserAlreadyExistsError(schema.username)

        user = User(
            username=schema.username,
            fullname=schema.fullname,
            hash_password=schema.password, # TODO add bcrypt
            role=schema.role
        )

        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserViewDTO.model_validate(user)

        
    async def get_by_id(self, id: int) -> UserViewDTO:

        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)

        return UserViewDTO.model_validate(user)


    async def get_all(self) -> UserListDTO:

        users = await self.user_repository.get_all()

        return UserListDTO(
            count=len(users),
            items=[UserViewDTO.model_validate(user) for user in users]
        )


    async def delete(self, id: int) -> None:
        
        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)
    
        async with self.session.begin():
            await self.user_repository.delete(user)


    async def change_fullname(self, id: int, fullname: str) -> UserUpdateFullnameDTO:

        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)

        user.fullname = fullname
        
        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserUpdateFullnameDTO.model_validate(user)


    async def change_password(self, id: int, password: str) -> UserUpdatePasswordDTO:

        user = await self.user_repository.get_by_id(id)
        
        if user is None:
            raise UserNotFoundError(id)

        user.hash_password = password # TODO add bcrypt
        
        async with self.session.begin():
            user = await self.user_repository.save(user)

        return UserUpdatePasswordDTO.model_validate(user)
