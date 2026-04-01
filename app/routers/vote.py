from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/")
async def handle_voting(payload: schemas.VotePayload, db: Session=Depends(database.get_db), current_user: dict=Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id==payload.post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {payload.post_id} was not found.")

    db_vote_query = db.query(models.Vote).filter(models.Vote.post_id==payload.post_id, models.Vote.user_id==current_user.id)
    db_vote = db_vote_query.first()
    
    if payload.dir == True:
        if db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user has already voted on this post with id {payload.post_id}")

        new_vote = models.Vote(post_id=payload.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return { "message": "Successfully added vote"}
    else:
        if not db_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="")
        db_vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Successfully deleted the vote."
        }