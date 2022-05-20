#Import FastApi components
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List

#Import Session from ORM
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import Pydantic schemas. Ensure that all SQLAlchemy models have their
# complementary schemas 
from app.schemas import *
from app.database import *
from app import models
from app.oauth2 import *

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

#Using List from the Typing library will return a list of posts not dict of posts
@router.get("/", response_model=List[PostVotes])
def get_posts(db: Session = Depends(get_db), current_user: int=Depends(get_current_user),
            limit: int=10, skip: int=0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get("/{id}", response_model=PostVotes)
def get_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found!")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: CreatePost, db: Session = Depends(get_db), 
                current_user: int=Depends(get_current_user)):
    """
    Each post should have a title and content in sting format.
    We pass Pydamtic's BaseModel to a variable called post.
    FastAPI will validate the POST data using the Post class.
    Since post is a pydantic class instance to refer to variables use the 
    dot notation (post.title etc.). It can be converted to dict in-place using
    post.dict().

    We dont use f-strings to sed SQL queries since they are susceptible to 
    SQL injection attacks. Using the placeholder method allows psycopg2 to 
    assert the inputs.   
    """

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session=Depends(get_db),
                current_user: int=Depends(get_current_user)):
    """
    Find the index of the item to delete from the 
    my_posts list using list.pop() method. 
    """

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action!")

    post_query.delete(synchronize_session=False)

    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, status_code=status.HTTP_201_CREATED, 
                db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action!")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()