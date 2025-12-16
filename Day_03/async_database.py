from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:your_password@localhost/your_db"

engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency - context manager pattern
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


# Creating the Tables:----

import asyncio
from database import engine, Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


#  CRUD Operations:-----

#1. CREATE:-------

from models import User
from database import get_async_session
from sqlalchemy.exc import SQLAlchemyError

async def create_user():
    async for session in get_async_session():
        try:
            new_user = User(name="Shiva", email="shiva@email.com")
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # refresh from DB (get id)
            print(f"User created: {new_user.id}")
        except SQLAlchemyError as e:
            await session.rollback()
            print("Error:", e)

#2. READ:-----
from sqlalchemy import select

async def get_users():
    async for session in get_async_session():
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(users)
#3. UPDATE :------
from sqlalchemy import update

async def update_user_email(user_id, new_email):
    async for session in get_async_session():
        await session.execute(
            update(User).where(User.id == user_id).values(email=new_email)
        )
        await session.commit()

#4. DELETE:----
from sqlalchemy import delete

async def delete_user(user_id):
    async for session in get_async_session():
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
