from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.database import get_async_session

router = APIRouter(prefix="/auth", tags=["auth"])

# Важно: схемы должны совпадать с теми, которыми ты хешировал пароль при регистрации
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_async_session)):
    # 1. Ищем пользователя
    stmt = select(User).where(User.email == request.username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    # Если пользователя нет — сразу 401 (не пытаемся читать пароль)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Если хеш пустой — тоже 401, а не 500
    if not user.hashed_password:
        raise HTTPException(status_code=401, detail="User exists but password is not set")

    # 2. Проверяем пароль
    is_valid = pwd_context.verify(request.password, user.hashed_password)
    
    if not is_valid:
        # Это правильный ответ, если пароль не совпал (даже если он 290522)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. Если всё ок — возвращаем токен
    return {
        "access_token": "real-jwt-token-will-be-here-later",
        "token_type": "bearer"
    }
