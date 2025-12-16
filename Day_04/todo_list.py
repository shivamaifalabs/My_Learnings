from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="My TO-DO List:--")

# Storing here and, not in DB:---
todos: List["Todo"] = []


class Todo(BaseModel):
    id: int = Field(..., gt=0, description="Must provide the ID")
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Description is Optional!"
    )
    completed: bool = False


class Todo_Response(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool



# 1. GET ALL TODOS
@app.get("/todo", response_model=List[Todo_Response], status_code=status.HTTP_200_OK)
def get_todos():
    return todos


# 2. GET A TODO BY ID
@app.get("/todo/{todo_id}", response_model=Todo_Response)
def get_single_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found!")


# 3. CREATE A TODO (POST)
@app.post("/todo", response_model=Todo_Response, status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    # Prevent duplication:--
    for t in todos:
        if t.id == todo.id:
            raise HTTPException(status_code=400, detail=" TODO ID already exists!")

    todos.append(todo)
    return todo


# 4. UPDATE A TODO (PUT)
@app.put("/todo/{todo_id}", response_model=Todo_Response)
def update_todo(todo_id: int, updated_data: Todo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = updated_data
            return updated_data

    raise HTTPException(status_code=404, detail="Todo not found!")


# 5. DELETE A TODO
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return

    raise HTTPException(status_code=404, detail="Todo not found!")
