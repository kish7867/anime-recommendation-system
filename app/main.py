from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.user import routes as user_routes
from app.anime import routes as anime_routes
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

# ✅ Root route to handle "/"
@app.get("/")
def read_root():
    return {"message": "Welcome to the Anime Recommender API!"}

# Include API routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(anime_routes.router)
