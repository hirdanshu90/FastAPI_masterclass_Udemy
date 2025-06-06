from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from router import blog_get, blog_post, user, article, product, file
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)


@app.get('/hello')
def index():
  return {'message': 'Hello world!'}



# Exception Handler
@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
  return JSONResponse(
    status_code= 418,
    content= {'detail': exc.name}
  )
  
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#   return PlainTextResponse(str(exc), status_code = status.HTTP_400_BAD_REQUEST)
  

# Create Database
models.Base.metadata.create_all(engine)

origins = [
    "https://example.com",
    "https://another-domain.com"
]

# CORS 
app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ['*'],
  allow_headers = ['*'],
)