from typing import List
from pydantic import BaseModel, EmailStr

# Articles inside UserDisplay
#  Represents the structure for an article when it’s displayed as part of a user.
class Articles(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        orm_mode =True
   
   
 # Represents the structure of an article when creating a new article (input schema).  
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool  
    creator_id: int  
    
# User inside Article display 
# Purpose: This class is embedded within ArticleDisplay to show basic user information associated with an article.

class user(BaseModel):
    id: int
    username : str
    class Config():
        orm_mode =True
    
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool  
    user: user  
    class Config():
        orm_mode =True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    
class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Articles] = []
    class Config():
        orm_mode =True
        
class ArticleWithUser(BaseModel):
    article: ArticleDisplay
    current_user: UserBase