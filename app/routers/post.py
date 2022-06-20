from typing import List
from unittest import result
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import engine, get_db
from .. import models, schemas, utils, oauth2

router = APIRouter()

# @router.get("/posts", response_model=List[schemas.Post])
@router.get("/posts", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str | None = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/posts/own", response_model=List[schemas.PostOut])
def get_own_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()
    # return db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()



@router.get('/posts/{post_id}', response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post




@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    print(current_user.id, current_user.email)
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    updated_post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = updated_post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
    
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post




@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()



