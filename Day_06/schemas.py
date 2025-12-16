
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=72)
    full_name: Optional[str] = None
    role:Optional[str]=None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    model_config = {
        "from_attributes": True   # replaces orm_mode=True in Pydantic v2
    }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenWithRefresh(Token):
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    user_id: int
    email: Optional[str] = None
    role: Optional[str] = None
    exp: int
    jti: str


