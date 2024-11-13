from sqlalchemy.orm.session import Session
from db.models import DbUser
from schemas import UserBase
from db.hash import Hash 

from fastapi import HTTPException, status


# Purpose: Contains the function for creating a new user in the database.

def create_user(request: UserBase, db: Session):
    try:
        new_user = DbUser(
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


def get_all_users(db: Session):
    try:
        return db.query(DbUser).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    
def get_user(db: Session, id: int ):
    try: 
        user = db.query(DbUser).filter(DbUser.id == id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error fetching users: {str(e)}")
    
def get_user_by_username(db: Session, username: str ):
    try: 
        user = db.query(DbUser).filter(DbUser.username == username).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error fetching users: {str(e)}")
    

def update_user(db: Session, id: int, request: UserBase):
    try:
        user = db.query(DbUser).filter(DbUser.id == id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update each attribute individually
        user.username = request.username
        user.email = request.email
        user.password = Hash.bcrypt(request.password)

        db.commit()
        db.refresh(user)  # Refresh to get updated data
        return user  # Return the updated user instance for response

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")
    
    
def delete_user(db: Session, id: int):
    try:
        user = db.query(DbUser).filter(DbUser.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
  
        db.delete(user)
        db.commit()
        return {"message": "User deleter"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")