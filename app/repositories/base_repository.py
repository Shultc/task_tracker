from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, Generic, TypeVar, List, Optional

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_by_id(self, id_: int, model: Type[T]) -> Optional[T]:
        result = await self.session.execute(select(model).where(model.id == id_))
        return result.scalars().first()

    async def list_all(self, model: Type[T]) -> List[T]:
        result = await self.session.execute(select(model))
        return list(result.scalars())
