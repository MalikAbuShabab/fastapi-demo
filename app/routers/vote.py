from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from .. import schemas,   database, models , oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/vote",
    tags=['Vote']
)

@router.post("/", status_code = status.HTTP_200_OK)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
                current_user: int  = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.user_id)
    found_vote = vote_query.first()

    if  (vote.dir  == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="You have already voted for this post")
         
        vote = models.Vote(post_id=vote.post_id, user_id=current_user.user_id)
        db.add(vote)
        db.commit()

        return {"success": True, "message": "Vote added"}
    #     # return Response(status_code=status.HTTP_200_OK)
        
    elif (vote.dir == 0):
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vote not found")
        
        vote_query.delete()
        db.commit()

        # return Response(status_code=status.HTTP_200_OK)
        return {"success": True, "message": "Vote deleted"}
    else:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Invalid vote direction")

        