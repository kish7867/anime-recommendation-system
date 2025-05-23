# SEARCH AND RECOMMENDATIONS 

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, models
from app.anime.anilist import search_anime
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/anime", tags=["Anime"])

def get_user(token: str, db: Session):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    return db.query(models.User).filter(models.User.username == username).first()

@router.get("/search")
async def search(name: str = None, genre: str = None):
    return await search_anime(name=name, genre=genre)

@router.get("/recommendations")
async def recommend(token: str = Depends(oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    user = get_user(token, db)
    genres = user.preferences.split(",") if user.preferences else []
    all_results = []
    for genre in genres:
        results = await search_anime(genre=genre.strip())
        all_results.extend(results)
    return all_results
