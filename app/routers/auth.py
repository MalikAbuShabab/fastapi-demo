from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session



from .. import models, schemas, utils,database, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login",)
def login( user_credentials: schemas.UserLogin ,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
         detail=f"user with email : {user_credentials.email} was not found")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail="Incorrect credentials")

    # create jwt token
    access_token =  oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}