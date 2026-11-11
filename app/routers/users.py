from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
# ЭТОТ ИМПОРТ КРИТИЧЕСКИ ВАЖЕН: без него Python не знает, что такое User
from app.models.user import User  

router = APIRouter(prefix="/users", tags=["users"])

async def get_user_repo(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repo)
):
    existing_user = await repo.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create_user(user_data)

@router.get("/", response_model=list[UserResponse])
async def list_users(repo: UserRepository = Depends(get_user_repo)):
    users = await repo.list_users()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    # Ключевое исправление: передаём и ID, и модель User, как требует BaseRepository
    user = await repo.get_by_id(user_id, User)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: dict,
    repo: UserRepository = Depends(get_user_repo)
):
    user = await repo.get_by_id(user_id, User)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "name" in user_update:
        user.name = user_update["name"]
    if "email" in user_update:
        existing = await repo.get_user_by_email(user_update["email"])
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = user_update["email"]

    await repo.session.flush()
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    deleted = await repo.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
