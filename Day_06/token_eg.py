from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify:--
from jose import jwt, JWTError

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains user_id, role, exp
    except JWTError:
        raise Exception("Invalid token")


# How Client- sends TOKENS:--
'''fetch("/profile", {
  headers: {
    "Authorization": "Bearer " + token
  }
})
'''

# How FastAPI Extract Tokens from Backend:--

'''
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ( Authorization: Bearer <token> )

token = oauth2_scheme(request)

# Token Used By the Function:-

def get_current_user(token: str = Depends(oauth2_scheme)):

'''


# Code:--

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from DB (pseudo example)

        # user = get_user_by_id(user_id)
        # return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Any Protected Routes will use like this:--
app=FastAPI()

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return {"msg": "Hello", "user": user}


# Token Expiry:-------------------------

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
