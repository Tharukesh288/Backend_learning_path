from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()     #This creates your web application.

# Path Parameter

@app.get("/")       #@app is the decorator If someone sends a GET request to /profile, use the function below to handle it.
def home():
    return {"message":"Hello World"}

@app.get("/profile")
def profile():
    return{
        "name":"Tharukesh",
        "age":20,
        "course":"Backend Development"
    }

@app.get("/favorite_language")
def favorite_language():
    return{
        "favorite_language":"Python"
    }

# Dynamic routes

@app.get("/users/{user_id}")    #the {} tells this part of URL is dynamic 
def get_user(user_id:int):      
    return{
        "user_id":user_id,
        "message":f"user {user_id} found"
    }

@app.get("/product/{product_id}")
def get_product(product_id:int):
    return{
        "product_id":product_id,
        "message": f"product ID is {product_id}"
    }

@app.get("/square/{value}")
def square(value:int):
    return{
        "given value is":value,
        "square value is":value*value
    }

@app.get("/cube/{value}")
def cube(value:int):
    return{
        "given value is":value,
        "cube value is":value*value*value
    }

# Query Parameter
@app.get("/search")     # there is no {name} FastAPI sees that name isn't in the path, so it treats it as a query parameter.
def search(name:str):
    return{
        "search":name
    }

@app.get("/search/{search_id}")
def search(name:str,search_id:int):
    return{
        "search":name,
        "search-id":search_id
    }

@app.get("/add")
def values(first:int,second:int):
    return{
        "num1": first,
        "num2":second,
        "sum":first+second
    }

@app.get("/subtract")
def values(first:int,second:int):
    return{
        "num1": first,
        "num2":second,
        "subtract":first-second
    }

@app.get("/multiply")
def values(first:int,second:int):
    return{
        "num1": first,
        "num2":second,
        "multiply":first*second
    }

@app.get("/divide")
def values(first:int,second:int):
    return{
        "num1": first,
        "num2":second,
        "divid":first/second
    }

# POST 

class User(BaseModel):      # You're defining the structure of the expected JSON and you are inheriting BaseModel from the FastAPI 
    name:str
    age:int

@app.post("/user")          # you run it with the url /user/docs
def create_user(user:User): # Read the request body and convert it into a User object
    return{
        "message":"user ID created",
        "user":user
    }

