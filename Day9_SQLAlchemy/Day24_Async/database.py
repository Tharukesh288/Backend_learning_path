from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "postgresql+asyncpg://backend_user:1%40Tharukesh@localhost/backend_db"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)