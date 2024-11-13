from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import oauth2_scheme, SECRET_KEY, ALGORITHM

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username : str = payload.get('sub')

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db_user.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
    
    # try:
    #     # Decode the JWT token
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     username: str = payload.get("sub")
    #     if username is None:
    #         raise credentials_exception
    # except JWTError:
    #     raise credentials_exception
    
    # # Retrieve the user from the database
    # user = db.query(DbUser).filter(DbUser.username == username).first()
    # if user is None:
    #     raise credentials_exception
    # return user
