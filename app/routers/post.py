from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import engine, get_db
from ..import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
    
@router.get("/"
            , response_model=List[schemas.PostResponse]
        )
async def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str] = ""):
    """Retrieve all posts."""
    if limit < 0:
        limit = 0
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)
    # ).limit(limit).offset(skip).all()
    
    results = db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Post.id==models.Vote.post_id,
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()
    # print(results[0].votes)
    return results

@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Retrieve a post by id."""
    # post = db.query(models.Post).where(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).where(id==models.Post.id).first()
    if not post:
        detail = f"The post with id {id} not found."
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Create a new post."""
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Delete a post by id."""
    post_to_delete = db.query(models.Post).where(models.Post.id == id).first()
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found!")
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform this action")
        
    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Update a post by id."""
    # 1. Fetch the actual object from the DB
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    # 2. Check if the post exists
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
        
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform this action")

    # 3. Update the attributes using the data from the request body
    # Using .dict() or .model_dump() (Pydantic v2)
    post_query.update(post.model_dump(), synchronize_session=False)
    
    # 4. Commit and return the updated object
    db.commit()
    db.refresh(db_post)
    return db_post

