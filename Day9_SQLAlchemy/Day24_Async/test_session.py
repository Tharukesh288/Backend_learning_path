import asyncio

from sqlalchemy import text

from database import AsyncSessionLocal


async def test_session():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))

        print(result.scalar())


asyncio.run(test_session())
