from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/vote", status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")
    
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} have already voted for {vote.post_id} post")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "Vote created successfully"
        } 
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} have not voted for {vote.post_id} post")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Vote deleted successfully"
        }