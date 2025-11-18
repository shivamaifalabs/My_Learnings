# Query - Parameters:--
from fastapi import Query,FastAPI,Path,Body,status
from pydantic import BaseModel

app=FastAPI(title="Query Parameters!")


class Payload(BaseModel):
    author:str
    
@app.post("/products/{id}")
def get_products(
    id:int=Path(...,gt=0,le=50,description="Book ID must be positive and <=50!"),
    name:str=Query(...,description="Book name must be there!"),
    Payload:Payload=Body(...,description="carrying payloads from 'BODY' ")
    ):
    return {"id":id,"name":name,"author":Payload.author}

#url= http://127.0.0.1:8000/products/1?name=python



# Response Model:----

#without response-model:--
@app.get("/user")
def get_user():
    return {"id": 1, "name": "John", "password": "1234"}

#with response model & Status Code:--
class User_Response(BaseModel):
    id:int
    name:str

@app.get("/user",response_model=User_Response,status_code=status.HTTP_200_OK)
def get_user(res):
    return {"id": 1, "name": "John", "password": "1234"}
