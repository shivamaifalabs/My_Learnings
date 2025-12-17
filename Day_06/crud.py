
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app import models
from app.schemas import UserCreate
from datetime import datetime,timezone


async def get_user_by_email(db: AsyncSession, email: str):
    q = await db.execute(select(models.User).where(models.User.email == email))
    return q.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    q = await db.execute(select(models.User).where(models.User.id == user_id))
    return q.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate, hashed_password: str):
    user_obj = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role if user_in.role else "user"
    )
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj

# Refresh token CRUD
async def create_refresh_token_record(db: AsyncSession, jti: str, user_id: int, expires_at: datetime):
    rt = models.RefreshToken(jti=jti, user_id=user_id, expires_at=expires_at, revoked=False)
    db.add(rt)
    await db.commit()
    await db.refresh(rt)
    return rt

async def get_refresh_token_by_jti(db: AsyncSession, jti: str):
    q = await db.execute(select(models.RefreshToken).where(models.RefreshToken.jti == jti))
    return q.scalar_one_or_none()


async def revoke_refresh_token(db: AsyncSession, jti: str):
    q = await db.execute(select(models.RefreshToken).where(models.RefreshToken.jti == jti))
    rt = q.scalar_one_or_none()
    if not rt:
        return None
    rt.revoked = True
    db.add(rt)
    await db.commit()
    return rt

async def is_refresh_token_revoked(db: AsyncSession, jti: str) -> bool:
    rt = await get_refresh_token_by_jti(db, jti)
    if not rt:
        return True  # treat missing token as revoked/invalid
    now = datetime.now(timezone.utc)
    return rt.revoked or (rt.expires_at < now)

# Token blacklist
async def add_token_to_blacklist(db: AsyncSession, jti: str, expires_at: datetime):
    tb = models.TokenBlacklist(jti=jti, expires_at=expires_at)
    db.add(tb)
    await db.commit()
    return tb

async def is_token_blacklisted(db: AsyncSession, jti: str) -> bool:
    q = await db.execute(select(models.TokenBlacklist).where(models.TokenBlacklist.jti == jti))
    return q.scalar_one_or_none() is not None
