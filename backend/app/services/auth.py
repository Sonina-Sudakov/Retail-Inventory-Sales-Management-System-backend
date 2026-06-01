from app.core.auth.security import create_access_token, verify_password
from app.db.repositories.user import UserRepository
from app.schemas.login import LoginSchema
from app.services.exceptions import InvalidCredentialsError


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository
    ):

        self.user_repository = user_repository


    async def login(
        self,
        schema: LoginSchema,
    ) -> str:

        user = await self.user_repository.get_by_username(
            schema.username
        )

        if not user:
            raise InvalidCredentialsError()

        hash_password = await self.user_repository.get_user_password_hash(user.id)

        if not verify_password(
            schema.password,
            hash_password
        ):

            raise InvalidCredentialsError()

        return create_access_token(user)
