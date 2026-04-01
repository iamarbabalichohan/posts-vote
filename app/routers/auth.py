from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    password_check = utils.verify_password(user.password, db_user.password)
    if not password_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data = {
        "user_id": db_user.id
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }