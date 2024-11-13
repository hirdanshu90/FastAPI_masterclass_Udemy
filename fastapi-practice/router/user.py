from typing import List, Optional
from fastapi import APIRouter, Body, Depends, FastAPI, Path, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from schemas import UserBase, UserDisplay
from db import db_user
from auth import token_validation

router = APIRouter(
    prefix = "/user",
    tags = ['user']
)

# Create user
@router.post('/', response_model= UserDisplay)
async def create_the_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)

# Read all Users
@router.get('/', response_model= List[UserDisplay])
async def get_all_users(db:Session = Depends(get_db), current_user: UserDisplay = Depends(token_validation.get_current_user)):
    return db_user.get_all_users(db)

# Retrieve one user
@router.get('/{id}', response_model= UserDisplay)
async def get_user(id: int, db:Session = Depends(get_db)):
    return db_user.get_user(db, id)


# Update the user
@router.put('/{id}/update/', response_model= UserDisplay)
async def update_user(id: int,  request: UserBase, db:Session = Depends(get_db), current_user: UserDisplay = Depends(token_validation.get_current_user)):
    return db_user.update_user(db, id, request)

# Delete the user
@router.delete('/{id}/delete/')
async def delete_this_user(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(token_validation.get_current_user)):
    return db_user.delete_user(db,id)