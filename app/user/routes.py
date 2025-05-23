from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, models
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/user", tags=["User"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class PreferenceRequest(BaseModel):
    genres: List[str]

@router.post("/preferences")
def set_preferences(
    pref: PreferenceRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.SessionLocal)
):
    user = get_user(token, db)
    user.preferences = ",".join(pref.genres)
    db.commit()
    return {"message": "Preferences updated!"}
