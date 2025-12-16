from fastapi import Depends,FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


app=FastAPI()

engine = create_engine("database:///./test.db")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos")
def get_todos(db = Depends(get_db)):
    return db.query("Todo").all()
