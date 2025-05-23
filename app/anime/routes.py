from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, models
from app.anime.anilist import search_anime
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/anime", tags=["Anime"])

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

@router.get("/search")
async def search(name: str = None, genre: str = None):
    # Pass params directly, improved filtering and case-insensitive handled inside search_anime
    results = await search_anime(name=name, genre=genre)
    if not results:
        return []
    return results

@router.get("/recommendations")
async def recommend(token: str = Depends(oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    user = get_user(token, db)
    if not user.preferences:
        # Optional: return empty or default popular anime list if no preferences set
        return []
    
    genres = [g.strip() for g in user.preferences.split(",") if g.strip()]
    all_results = []

    for genre in genres:
        results = await search_anime(genre=genre)
        if results:
            all_results.extend(results)
    
    # Optionally deduplicate anime by title romaji to avoid repeats
    seen_titles = set()
    unique_results = []
    for anime in all_results:
        title = anime.get("title", {}).get("romaji", "")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_results.append(anime)

    return unique_results
