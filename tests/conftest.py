import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_async_session

# Создаём движок один раз на всю сессию тестов
@pytest.fixture(scope="session")
def test_engine():
    # Используем aiosqlite в памяти — он не требует отдельного event_loop для create_engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )
    yield engine
    # При завершении сессии закроем все соединения
    import asyncio
    asyncio.run(engine.dispose())

@pytest.fixture
async def test_session(test_engine):
    # Создаём таблицы при первой сессии (можно и в session scope, но так проще)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(test_session):
    app.dependency_overrides[get_async_session] = lambda: test_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
