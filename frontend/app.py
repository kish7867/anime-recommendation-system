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

# Get Recommendations (Robust Version)
elif option == "Get Recommendations":
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        r = requests.get(f"{BASE_URL}/anime/recommendations", headers=headers)
        
        try:
            results = r.json()
        except Exception as e:
            st.error(f"Failed to parse response JSON: {e}")
            results = None

        if not results:
            st.warning("🤷 No recommendations available.")
        else:
            # If results is a dict, try to find the list of recommendations inside it
            if isinstance(results, dict):
                possible_keys = ["data", "results", "recommendations"]
                for key in possible_keys:
                    if key in results:
                        results = results[key]
                        break
                else:
                    st.warning("🤷 No valid recommendations data found in the response.")
                    results = []

            # If still not a list, warn and clear results
            if not isinstance(results, list):
                st.warning("🤷 Unexpected recommendations format received.")
                results = []

            # Loop through the recommendations safely
            for anime in results:
                if not isinstance(anime, dict):
                    continue  # skip if not a dict

                title_info = anime.get("title", {})
                if isinstance(title_info, dict):
                    title = title_info.get("romaji", "N/A")
                else:
                    title = str(title_info) if title_info else "N/A"

                genres_list = anime.get("genres", [])
                genres = ", ".join(genres_list) if isinstance(genres_list, list) else "N/A"

                popularity = anime.get("popularity", "N/A")

                st.info(
                    f"""
                    **🎬 Title:** {title}  
                    **📚 Genres:** {genres}  
                    **🔥 Popularity Score:** {popularity}
                    """
                )
