# frontend/app.py
import streamlit as st
import requests

BASE_URL = "https://anime-recommendation-system-1n3e.onrender.com/"  # update after deploying

st.title("🎌 Anime Recommendation System")

option = st.selectbox("Choose Action", ["Register", "Login", "Search Anime", "Get Recommendations", "Set Preferences"])

# Registration
if option == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        r = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "password": password})
        st.write(r.json())

# Login
elif option == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        r = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        st.session_state.token = r.json().get("access_token")
        st.success("✅ Logged in successfully!")

# Search Anime (Cleaned Output)
elif option == "Search Anime":
    name = st.text_input("Anime name")
    genre = st.text_input("Genre")
    if st.button("Search"):
        r = requests.get(f"{BASE_URL}/anime/search", params={"name": name, "genre": genre})
        results = r.json()

        if not results:
            st.warning("😕 No anime found.")
        else:
            for anime in results:
                title = anime.get("title", {}).get("romaji", "N/A")
                genres = ", ".join(anime.get("genres", []))
                popularity = anime.get("popularity", "N/A")

                st.success(
                    f"""
                    **🎬 Title:** {title}  
                    **📚 Genres:** {genres}  
                    **🔥 Popularity Score:** {popularity}
                    """
                )

# Set Preferences
elif option == "Set Preferences":
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first.")
    else:
        genres = st.text_input("Enter your favorite genres (comma separated)")
        if st.button("Save Preferences"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            r = requests.post(f"{BASE_URL}/user/preferences", json={"genres": genres.split(",")}, headers=headers)
            st.write(r.json())

# Get Recommendations (Cleaned Output)
elif option == "Get Recommendations":
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        r = requests.get(f"{BASE_URL}/anime/recommendations", headers=headers)
        results = r.json()

        if not results:
            st.warning("🤷 No recommendations available.")
        else:
            for anime in results:
                title = anime.get("title", {}).get("romaji", "N/A")
                genres = ", ".join(anime.get("genres", []))
                popularity = anime.get("popularity", "N/A")

                st.info(
                    f"""
                    **🎬 Title:** {title}  
                    **📚 Genres:** {genres}  
                    **🔥 Popularity Score:** {popularity}
                    """
                )
