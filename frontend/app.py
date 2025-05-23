import streamlit as st
import requests

BASE_URL = "https://anime-recommendation-system-1n3e.onrender.com/"

st.title("🎌 Anime Recommendation System")

option = st.selectbox("Choose Action", ["Register", "Login", "Search Anime", "Get Recommendations", "Set Preferences"])

# Registration
if option == "Register":
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()
    if st.button("Register") and username and password:
        with st.spinner("Registering..."):
            r = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "password": password})
        if r.status_code == 200:
            st.success("Registration successful!")
        else:
            st.error(f"Registration failed: {r.json().get('detail', r.text)}")

# Login
elif option == "Login":
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()
    if st.button("Login") and username and password:
        with st.spinner("Logging in..."):
            r = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        if r.status_code == 200:
            token = r.json().get("access_token")
            if token:
                st.session_state.token = token
                st.success("✅ Logged in successfully!")
            else:
                st.error("Login failed: No token received.")
        else:
            st.error(f"Login failed: {r.json().get('detail', r.text)}")

# Search Anime
elif option == "Search Anime":
    name = st.text_input("Anime name").strip()
    genre = st.text_input("Genre").strip()
    if st.button("Search") and (name or genre):
        with st.spinner("Searching..."):
            # Convert name to lowercase to help case insensitive search
            r = requests.get(f"{BASE_URL}/anime/search", params={"name": name.lower(), "genre": genre})
        if r.status_code == 200:
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
        else:
            st.error(f"Search failed: {r.text}")

# Set Preferences
elif option == "Set Preferences":
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first.")
    else:
        genres = st.text_input("Enter your favorite genres (comma separated)").strip()
        if st.button("Save Preferences") and genres:
            genre_list = [g.strip() for g in genres.split(",") if g.strip()]
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            with st.spinner("Saving preferences..."):
                r = requests.post(f"{BASE_URL}/user/preferences", json={"genres": genre_list}, headers=headers)
            if r.status_code == 200:
                st.success("Preferences saved!")
            else:
                st.error(f"Failed to save preferences: {r.text}")

# Get Recommendations
elif option == "Get Recommendations":
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first.")
    else:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        with st.spinner("Getting recommendations..."):
            r = requests.get(f"{BASE_URL}/anime/recommendations", headers=headers)
        if r.status_code == 200:
            try:
                results = r.json()
            except Exception as e:
                st.error(f"Failed to parse response JSON: {e}")
                results = None

            if not results:
                st.warning("🤷 No recommendations available.")
            else:
                # If results is a dict, try to find the list inside it
                if isinstance(results, dict):
                    for key in ["data", "results", "recommendations"]:
                        if key in results:
                            results = results[key]
                            break
                    else:
                        st.warning("🤷 No valid recommendations data found in the response.")
                        results = []

                if not isinstance(results, list):
                    st.warning("🤷 Unexpected recommendations format received.")
                    results = []

                for anime in results:
                    if not isinstance(anime, dict):
                        continue
                    title_info = anime.get("title", {})
                    title = title_info.get("romaji", "N/A") if isinstance(title_info, dict) else str(title_info)
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
        else:
            st.error(f"Failed to get recommendations: {r.text}")
