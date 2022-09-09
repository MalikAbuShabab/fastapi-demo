from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas,utils
#from fastapi_redis_cache import FastApiRedisCache, cache
from .. import oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import  List, Optional

router = APIRouter(
    prefix= "/posts",
    tags=["posts"]

)

  # Get  post list
@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db) ,user_id: int  = Depends(oauth2.get_current_user), Limit: int = 10, Offset: int = 0,
search : Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return posts

# Create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost,db: Session = Depends(get_db),
        current_user: int  = Depends(oauth2.get_current_user)):

    db_post = models.Post(owner_id = current_user.user_id,**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

# Get post by id
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int,db: Session = Depends(get_db),current_user: int  = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id : {id} was not found")

    return  post

# Delete post by id
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id : {id} was not found")

    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail=f"You are not authorized to delete this post")

    db.delete(post)
    db.commit()
    return  Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post by id
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.UpdatePost,db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    postt = post_query.first()

    if not postt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id : {id} was not found")

    if postt.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail=f"You are not authorized to update this post")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
