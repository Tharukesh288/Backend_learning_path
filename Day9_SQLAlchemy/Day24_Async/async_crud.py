import asyncio

from database import AsyncSessionLocal
from models import Book


async def delete_book():
    async with AsyncSessionLocal() as session:

        book = await session.get(Book, 6)

        if book:
            print(f"Deleting: {book.title}")

            await session.delete(book)

            await session.commit()

            print("Book deleted")


asyncio.run(delete_book())