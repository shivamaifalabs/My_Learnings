
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# helping to create tables on startup (optional)
async def create_all_tables():
    from app import models
    async with engine.begin() as conn:
        # Run the SQLAlchemy metadata.create_all in a sync context
        await conn.run_sync(models.Base.metadata.create_all)
