# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timezone
from jose import JWTError, ExpiredSignatureError

from app import crud, security
from app.schemas import (
    UserCreate,
    UserOut,
    TokenWithRefresh,
    RefreshRequest
)
from app.dependencies import get_db, oauth2_scheme, admin_required

router = APIRouter(prefix="/auth", tags=["auth"])



# REGISTER

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed = security.hash_password(user_in.password)
    user = await crud.create_user(db, user_in, hashed)
    return user



# LOGIN - returns access + refresh (OAuth2 form)

@router.post("/login", response_model=TokenWithRefresh)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # username == email in your app
    user = await crud.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    payload = {"user_id": user.id, "email": user.email, "role": user.role}

    access_token = security.create_access_token(payload)
    refresh_token = security.create_refresh_token(payload)

    # store refresh token record (jti + expiry)
    rt_payload = security.decode_token(refresh_token)
    rt_jti = rt_payload.get("jti")
    rt_exp = rt_payload.get("exp")
    expires_at = datetime.fromtimestamp(int(rt_exp), tz=timezone.utc)
    await crud.create_refresh_token_record(db, rt_jti, user.id, expires_at)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



# REFRESH (rotation)

@router.post("/refresh", response_model=TokenWithRefresh)
async def refresh_token(req: RefreshRequest, db: AsyncSession = Depends(get_db)):
    token = req.refresh_token
    try:
        payload = security.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")

    jti = payload.get("jti")
    user_id = payload.get("user_id")
    if not jti or not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token payload")

    # Fetch refresh token record
    rt = await crud.get_refresh_token_by_jti(db, jti)

    # FIXED: use timezone-aware datetime
    now = datetime.now(timezone.utc)

    if not rt or rt.revoked or rt.expires_at < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalid or revoked")

    # Revoke old RT
    await crud.revoke_refresh_token(db, jti)

    # Issue new tokens
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_payload = {"user_id": user.id, "email": user.email, "role": user.role}
    new_access = security.create_access_token(user_payload)
    new_refresh = security.create_refresh_token(user_payload)

    # Save new refresh token
    new_rt_payload = security.decode_token(new_refresh)
    new_jti = new_rt_payload.get("jti")
    new_exp = new_rt_payload.get("exp")

    # FIXED: timezone-aware expires_at
    new_expires_at = datetime.fromtimestamp(int(new_exp), tz=timezone.utc)

    await crud.create_refresh_token_record(db, new_jti, user.id, new_expires_at)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }




# LOGOUT - blacklist access token jti

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    from app.crud import add_token_to_blacklist
    from app.security import decode_token

    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        # access token already expired - nothing to blacklist
        return {"message": "Token already expired"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")

    # convert exp to datetime
    if isinstance(exp, (int, float)):
        expires_at = datetime.utcfromtimestamp(int(exp))
    else:
        expires_at = exp

    await add_token_to_blacklist(db, jti, expires_at)
    return {"message": "Successfully logged out"}



# ADMIN dashboard (role-protected)
@router.get("/admin/dashboard")
async def admin_dashboard(current_user = Depends(admin_required)):
    return {"message": "Welcome to Admin Dashboard!"}
