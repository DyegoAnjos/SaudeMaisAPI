from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from saudemaisapi.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_db():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
