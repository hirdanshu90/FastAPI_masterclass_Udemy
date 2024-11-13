from typing import List, Optional
from fastapi import APIRouter, Body, Cookie, Depends, FastAPI, Form, Header, Path, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay
from db import db_article
from fastapi.responses import Response

router = APIRouter(
    prefix = "/product",
    tags = ['product']
)


products = ['watch', 'camera', 'phone']

@router.get('/all')
async def get_all_products():
    data = " ".join(products)
    response =  Response(content=data, media_type= 'text/plain')
    response.set_cookie(key = "test_cookie", value = "test_cookie_value")
    return response

 
 
@router.get('/withheader')
def get_products(response: Response, 
                 custom_header: Optional[List[str]] = Header(None), 
                 test_cookie: Optional[str] = Cookie(None),
                 ):
    if custom_header:
        response.headers['Custom_response_header'] = " and ".join(custom_header)
    return {
        'data': products,
        'custom_header': custom_header,
        'my_cookie': test_cookie
        
    }
    
    
# Using this, one can input the data lets say in the product array defined above.
@router.post('/all')
def create_product(name: str = Form(...)):
    products.append(name)
    return products