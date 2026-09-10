from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from models import Book


app = FastAPI()


# -------------------------
# Database Dependency
# -------------------------

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# -------------------------
# Schemas
# -------------------------

class BookCreate(BaseModel):
    title: str
    pages: int
    price: float
    description: str | None = None
    author_id: int


class BookUpdate(BaseModel):
    title: str
    pages: int
    price: float
    description: str | None = None
    author_id: int


# -------------------------
# READ ALL
# -------------------------

@app.get("/books")
async def get_books(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Book)
    )

    books = result.scalars().all()

    return books


# -------------------------
# READ ONE
# -------------------------

@app.get("/books/{book_id}")
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# -------------------------
# CREATE
# -------------------------

@app.post("/books")
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
):
    book = Book(
        title=book_data.title,
        pages=book_data.pages,
        price=book_data.price,
        description=book_data.description,
        author_id=book_data.author_id
    )

    db.add(book)

    await db.commit()

    await db.refresh(book)

    return book


# -------------------------
# UPDATE
# -------------------------

@app.put("/books/{book_id}")
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.title = book_data.title
    book.pages = book_data.pages
    book.price = book_data.price
    book.description = book_data.description
    book.author_id = book_data.author_id

    await db.commit()

    await db.refresh(book)

    return book


# -------------------------
# DELETE
# -------------------------

@app.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    await db.delete(book)

    await db.commit()

    return {
        "message": "Book deleted successfully"
    }