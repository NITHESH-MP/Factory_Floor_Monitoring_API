import jwt 
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
Algorithm = os.getenv("ALGORITHM")
expire_time = os.getenv("EXPIRE_TIME")

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    
    return password_hash.verify(
        plain_password,
        hashed_password
    )
    
def hash_password(password):
    return password_hash.hash(password)

def create_access_token(username):
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes = int(expire_time)
    )
    
    payload = {
        "sub": username,
        "exp": expire
    }
    
    token = jwt.encode(
        payload,
        secret_key,
        algorithm= Algorithm
    )
    
    return token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[Algorithm]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
