# Anime Recommendation System 🎌

This is a REST API-based Anime Recommendation System built using **FastAPI**, **PostgreSQL**, and the **AniList GraphQL API**. It includes JWT-based authentication and user-specific anime preferences.

---

## 🔧 Features

- 🔍 Search for anime by name or genre.
- 🧠 Get personalized anime recommendations based on user preferences.
- 🔐 JWT-based authentication.
- 💾 PostgreSQL database for user and preference management.
- 🌐 Uses the AniList GraphQL API for real-time anime data.

---

## 🚀 Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (Python-Jose)
- Passlib
- HTTPX
- AniList GraphQL API

---

## 📁 Project Structure

anime-recommender/
├── app/
│ ├── auth/ # JWT auth logic
│ ├── anime/ # AniList API calls + routes
│ ├── user/ # User preference management
│ ├── main.py # FastAPI app entry point
│ ├── models.py # DB models
│ ├── schemas.py # Pydantic schemas
│ ├── config.py # Env + settings
│ ├── database.py # DB connection
├── alembic/ # Migrations
├── .env # Environment variables (DO NOT PUSH TO GITHUB)
├── .gitignore
├── frontend/app.py
│ ├── auth
├── requirements.txt
├── README.md

yaml
Copy
Edit


---

## 🧪 API Endpoints

| Method | Endpoint               | Description                      | Auth Required |
|--------|------------------------|----------------------------------|---------------|
| POST   | /auth/register         | Register a new user              | ❌            |
| POST   | /auth/login            | Login and get JWT token          | ❌            |
| POST   | /user/preferences      | Set favorite genres              | ✅            |
| GET    | /anime/search          | Search anime by name or genre    | ❌            |
| GET    | /anime/recommendations | Get anime recommendations        | ✅            |

---

## ⚙️ Setup Instructions

### 1. Clone the repo

git clone https://github.com/your-username/anime-recommendation-system.git
cd anime-recommendation-system

2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup .env file
Create a .env file in the root:
DATABASE_URL=postgresql://postgres:yourpassword@localhost/anime_recommender
SECRET_KEY=supersecretkey

5. Run migrations
alembic upgrade head

6. Run the server
uvicorn app.main:app --reload

7.🌐 Run the Frontend
cd frontend
streamlit run app.py

📦 Sample Requests

Register
curl -X POST http://localhost:8000/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'

Login
curl -X POST http://localhost:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'

🧑‍💻 Author
Developed as part of a recruitment assignment using best practices in Python backend development.