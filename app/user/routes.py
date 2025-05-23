from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM
from app import models, schemas, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/user", tags=["User"])

def get_user_from_token(token: str, db: Session) -> models.User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return db.query(models.User).filter(models.User.username == username).first()
    except JWTError:
        return None

@router.post("/preferences", status_code=status.HTTP_200_OK)
def set_preferences(preferences: schemas.Preferences, db: Session = Depends(database.SessionLocal), token: str = Depends(oauth2_scheme)):
    """
    Set the user's anime genre preferences.
    """
    user = get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    if not preferences.genres:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Genres list cannot be empty")

    # Clean genres: strip whitespace
    cleaned_genres = [genre.strip() for genre in preferences.genres if genre.strip()]
    if not cleaned_genres:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Genres list cannot be empty after cleaning")

    user.preferences = ",".join(cleaned_genres)
    db.add(user)
    db.commit()
    return {"msg": "Preferences saved successfully"}
