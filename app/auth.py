'''
Authetication functions for FastAPI
'''

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt # for json web token 
from passlib.context import CryptContext # password hashing
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os

from .schemas import UserCreate
from .models import User
from .database import get_db

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

# password hashing using bcrypt algo
auth_router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# token creation
# data parameter accepts dictionary data
def create_access_token(data: dict):
    to_encode = data.copy() # creates a copy of data to prevent modification of original
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # set expiry time for token
    to_encode.update({'exp': expire}) # adds exp to token to store expiry time
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # uses secretkey and algorithm to encode the token securely, then return the JWT string and used for authentication

# password verification
# checks the plain password against the hashed password using passlib
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# get password hash
def get_password_hash(password):
    return pwd_context.hash(password)

# user authentication
async def authenticate_user(username: str, password: str, db: AsyncSession):
    # get the user based on username
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()

    # if user's password is equal to hashed password then return user 
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# function to get current user based on their token
async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    try:
        # decode the token using the secret_key and Algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        # if username doesnt exist throw an unauthorized error
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        # check the database for username and save first matching in result variable
        query = select(User).filter(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()

        # if the user does not exist, throw a 401 unauthorized error
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)