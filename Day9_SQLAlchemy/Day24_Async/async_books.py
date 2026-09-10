import asyncio

from sqlalchemy import select

from database import AsyncSessionLocal
from models import Book


async def get_books():
    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(Book)
        )

        books = result.scalars().all()

        for book in books:
            print(
                book.id,
                book.title,
                book.price
            )


asyncio.run(get_books())