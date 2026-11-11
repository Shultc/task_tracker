from sqlalchemy import select
from typing import Optional

from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from .base_repository import BaseRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        hashed_password = pwd_context.hash(user_data.password)

        db_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        await self.create(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
        )

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def list_users(self) -> list[User]:
        return await self.list_all(User)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id, User)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True
