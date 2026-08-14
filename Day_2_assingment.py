from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

# books = [
#     {"title": "Python", "author": "Alex", "pages": 300},
#     {"title": "FastAPI", "author": "John", "pages": 250},
#     {"title": "Django", "author": "John", "pages": 500},
# ]                                                             #fake memory database

books = [
    {
        "title": "Python",
        "author": "Alex",
        "pages": 300,
        "price": 500,
        "book_id": 101
    }
]

@app.get("/")
def mes():
    return{
        "message":"hello world"
    }

class Book(BaseModel):
    title:str
    author:str
    pages:int


@app.post("/book")
def create_book(addbook:Book):
    books.append(addbook)
    return{
        "message":"Book added",
        "book":addbook
    }

@app.get("/books")
def allbooks():
    return books

@app.get("/books/{book_id}")    #get details from the fake database
def book_id(book_id:int):

    if book_id < 0 or book_id >= len(books):
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return books[book_id]

@app.put("/books/{book_id}")    #updates the list 
def update_book(book_id:int,updated_book:Book):

    if book_id < 0 or book_id >= len(books):
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )
    
    books[book_id]=updated_book

    return {
         "message":"Book updated",
         "books":updated_book
    }

@app.delete("/books/{book_id}")    #delete the book from the fake database
def deleted_book(book_id:int):

    if book_id < 0 or book_id >= len(books):
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    deleted_book = books.pop(book_id)

    return {
        "message":"book deleted",
        "book": deleted_book
    }

@app.get("/bookslist")
def get_book(author:str=None):

    if author is None:
        return books

    result = []

    for book in books:
        if book["author"] == author :
            result.append(book)

    return result

@app.get("/bookslist")
def get_book(author:str=None,pages:int=None):

    result = []
    for book in books:

        if author is not None and book["author"] != author:    # using this way we can easyly filter the request
            continue

        if pages is not None and book["pages"] != pages:
            continue

        result.append(book)
    return result

# Response Model 

class BookResponse(BaseModel):
    title:str
    author:str
    pages:int

@app.get("/books_response_model",response_model=list[BookResponse])
def get_book():
    return books
