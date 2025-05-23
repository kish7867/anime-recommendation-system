# frontend/app.py
import streamlit as st
import requests

BASE_URL = "https://YOUR_RENDER_BACKEND_URL"  # update after deploying

st.title("🎌 Anime Recommendation System")

option = st.selectbox("Choose Action", ["Register", "Login", "Search Anime", "Get Recommendations", "Set Preferences"])

if option == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        r = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "password": password})
        st.write(r.json())

elif option == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        r = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        st.session_state.token = r.json().get("access_token")
        st.write("Logged in!")

elif option == "Search Anime":
    name = st.text_input("Anime name")
    genre = st.text_input("Genre")
    if st.button("Search"):
        r = requests.get(f"{BASE_URL}/anime/search", params={"name": name, "genre": genre})
        for anime in r.json():
            st.write(anime)

elif option == "Set Preferences":
    if "token" not in st.session_state:
        st.warning("Please login first.")
    else:
        genres = st.text_input("Enter your favorite genres (comma separated)")
        if st.button("Save Preferences"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            r = requests.post(f"{BASE_URL}/user/preferences", json={"genres": genres.split(",")}, headers=headers)
            st.write(r.json())

elif option == "Get Recommendations":
    if "token" not in st.session_state:
        st.warning("Please login first.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        r = requests.get(f"{BASE_URL}/anime/recommendations", headers=headers)
        for anime in r.json():
            st.write(anime)
