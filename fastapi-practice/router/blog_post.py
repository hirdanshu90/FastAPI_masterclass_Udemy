from typing import List, Optional
from fastapi import APIRouter, Body, FastAPI, Path, Query
from pydantic import BaseModel

router = APIRouter(
    prefix = "/blog",
    tags = ['blog']
)


class Image(BaseModel):
    url:str
    alias: str
    

class BlogModel(BaseModel):
    title: str
    content:str
    no_of_comments: int
    published: Optional[bool]
    tags: List[str] = []
    image: Optional[Image] = None


@router.post("/new/{id}")
async def create_blog(blog: BlogModel, id:int, version:int = 3):
    return {'id': id, 'data': blog, 'version': version}


@router.post("/new/{id}/comment/{comment_id}")
async def create_comment(
    blog: BlogModel, 
    id: int, 
    comment_title: int = Query(..., description="random description here", alias='commentTitle'),
    content: str = Body(..., min_length=6, regex='^[a-z\s]*$'),
    v: Optional[List[str]] = Query(None),
    comment_id: int = Path(..., gt=5, le=10),
    
):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        "content": content,
        'version': v,
        'comment_id': comment_id
    }


def required_functionality():
    return {"message": "Learing fastapi is important"}