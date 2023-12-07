from asyncio import current_task

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import DB_USER, DB_HOST, DB_PORT, DB_NAME, DB_PASSWORD, DEBUG

DATABASE_URL = \
    f'mysql+aiomysql://f{DB_USER}:f{DB_PASSWORD}@f{DB_HOST}:f{DB_PORT}/f{DB_NAME}?charset=utf8mb4'

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=DEBUG)

async_session_factory = sessionmaker(engine, class_=AsyncSession)

AsyncScopedSession = async_scoped_session(
    async_session_factory,
    scopefunc=current_task
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
