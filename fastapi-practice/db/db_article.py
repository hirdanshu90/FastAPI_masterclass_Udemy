from sqlalchemy.orm.session import Session
from db.models import DbArticle, DbUser
from schemas import UserBase, ArticleBase
from db.hash import Hash 

from fastapi import HTTPException, status
from exceptions import StoryException

def create_article(db: Session, request: ArticleBase):
    try:
        if request.content.startswith('Once upon  a time'):
            raise StoryException('No stories please')
        new_article = DbArticle(
            title = request.title,
            content = request.content,
            published = request.published,
            user_id = request.creator_id
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article
   
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))
       



def get_article(db: Session, id:int):
    try: 
        article = db.query(DbArticle).filter(DbArticle.id == id).first()
        if not article:
            raise Exception(status_code = status.HTTP_404_NOT_FOUND , detail = "article not found")
        return article
    except Exception as e:
            raise HTTPException(status_code=500, detail= f"Error fetching users: {str(e)}")

        
