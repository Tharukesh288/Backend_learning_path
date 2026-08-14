from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from database import create_table, add_book, get_books, get_book, update_book, delete_book

class Book(BaseModel):
    title:str
    author:str
    pages:int
    price:float

app = FastAPI()
create_table()

@app.get("/")
def home():
    return{
        "message":"FastAPI + SQLite is working"
    }

@app.post("/books")
def create_book(book:Book):
    add_book(book)

@app.get("/all_books")
def read_book():
    books = get_books()
    return books

@app.get("/books/{book_id}")
def read_book(book_id:int):
    book = get_book(book_id)

    if book is None :           # if the book variable didn't get any value it retruns None
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book

@app.put("/books/{book_id}")
def edit_book(book_id:int,book:Book):

    existing_book = get_book(book_id)

    if existing_book is None:
        raise HTTPException(
                    status_code=404,
                    detail="Book not found"
                )
    update_book(book_id,book)

    return {
        "message":"Book update successfully"
    }

@app.delete("/books/{book_id}")
def remove_book(book_id:int):
    existing_book=get_book(book_id)

    if existing_book is None:
            raise HTTPException(
                        status_code=404,
                        detail="Book not found"
                    )
    delete_book(book_id)

    return{
        "message":"Book deleted successfully"
    }