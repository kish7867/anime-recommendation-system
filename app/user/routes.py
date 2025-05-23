# USER PREFERENCES 

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM
from app import models, schemas, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/user", tags=["User"])

def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return db.query(models.User).filter(models.User.username == username).first()
    except JWTError:
        return None

@router.post("/preferences")
def set_preferences(preferences: schemas.Preferences, db: Session = Depends(database.SessionLocal), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=401)
    user.preferences = ",".join(preferences.genres)
    db.commit()
    return {"msg": "Preferences saved"}
