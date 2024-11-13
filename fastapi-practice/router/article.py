from typing import List, Optional
from fastapi import APIRouter, Body, Depends, FastAPI, Path, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay, ArticleWithUser, UserBase, UserDisplay
from db import db_article
from auth.oauth2 import oauth2_scheme
from db.models import DbUser
from auth import token_validation

router = APIRouter(
    prefix = "/article",
    tags = ['article']
)


# create Article
@router.post("/", response_model= ArticleDisplay)
async def create_article(request: ArticleBase, db: Session = Depends(get_db) , current_user: UserDisplay = Depends(token_validation.get_current_user)):
    return db_article.create_article(db, request)


# Read one Article

@router.get('/protected-article/{id}', response_model=ArticleWithUser)
async def get_protected_article(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(token_validation.get_current_user)):
    # Only accessible if token is valid and user exists
    
    # Fetch the article
    article = db_article.get_article(db, id)
    
    return {
        "article": ArticleDisplay(
            title=article.title,
            content=article.content,
            published=article.published,
            user={
                "id": article.user.id,
                "username": article.user.username
            }
        ),
        "current_user": current_user
    }









# # Update the user
# @router.put('/{id}/update/', response_model= UserDisplay)
# async def update_user(id: int,  request: UserBase, db:Session = Depends(get_db)):
#     return db_user.update_user(db, id, request)

# # Delete the user
# @router.delete('/{id}/delete/')
# async def delete_this_user(id: int, db: Session = Depends(get_db)):
#     return db_user.delete_user(db,id)