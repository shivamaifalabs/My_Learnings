from fastapi import FastAPI

app = FastAPI(title="FastAPI Testing & Learnings")

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/welcome")
def welcome():
    return {"message":"Hey!, Welcome"}


# Get
@app.get("/books")
def get_books():
    return {"message":"Got, All the Books!"}

# Create
@app.post("/books/{book_id}")
def create_books(book_id:int):
    return {"message":f"Book with Id: {book_id} is created!"}


#Update
@app.put("/books/{book_id}")
def update_books(book_id:int):
    return {"message":f"Book with Id: {book_id}is updated"}

#Delete
@app.delete("/books/{book_id}")
def delete_books(book_id:int):
    return {"message":f"Book with Id: {book_id}is deleted"}


# # Validation--Examples:---

# from enum import Enum

# class Category(str, Enum):
#     electronics = "electronics"
#     fashion = "fashion"
#     toys = "toys"


# @app.get("/products/{category}")
# def get_products(category: Category):
#     return {"category": category}


# #  Query Parameters and Request Body:--

# @app.get("/items")
# def get_items(limit:int,search:str | None=None):
#     return {"limit":limit,"search":search}

# #url= /items?limit=10&search=mobile

# # Query Parameters + Path Parameters Together:---

# @app.get("/users/{user_id}/orders")
# def user_orders(user_id: int, limit: int=10, sort: str | None = None):
#     return {
#         "user_id": user_id,
#         "limit": limit,
#         "sort": sort
#     }
# # url= /users/7/orders?limit=20&sort=desc



# # Using from Request Body  (Pydantic Model):---

# from pydantic import BaseModel

# class Student(BaseModel):
#     id:int
#     name:str
#     present:bool=True

# @app.post("/students")
# def create_students(student:Student):
#     return student
