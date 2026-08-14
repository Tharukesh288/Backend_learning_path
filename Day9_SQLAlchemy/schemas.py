from pydantic import BaseModel

class AuthorCreate(BaseModel):      # Data comming into API 
    name:str

class AuthorResponse(AuthorCreate): # Data going out of API 
    id:int
    name:str

    class config:
        from_attributes = True


class BookCreate(BaseModel):        # Schema used when a client wants to create a new book.
    title:str
    author_id:int
    pages:int
    price:float

class BookResponse(BookCreate):     # Inherits all fields from BookCreate.
    id:int
    title:str
    author_id:int
    author:AuthorResponse
    pages:int
    price:float

    class config:
        from_attributes = True

class BookSimpleResponse(BaseModel):
    id:int
    title:str
    pages:int
    price:float

    class config:
        from_attributes = True

class AuthorWithBookResponse(BaseModel):
    id:int
    name:str
    books:list[BookSimpleResponse]

    class config:
        from_attributes = True

class UserCreate(BaseModel):
    username:str
    password:str