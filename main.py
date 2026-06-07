# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download pkl files from Google Drive if not present
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1UDZxKauKeXqzJcARz9R66OW7N5BC2gxd", "similarity.pkl", quiet=False)

if not os.path.exists("movies_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=10KxE4vBFso484UY0RWkjTYISedIjN1CZ", "movies_dict.pkl", quiet=False)

if not os.path.exists("movies.pkl"):
    gdown.download("https://drive.google.com/uc?id=1OoMZlKFgcaj6BbYegbA_rxTbHohBjeuT", "movies.pkl", quiet=False)


FALLBACK_POSTER = "https://via.placeholder.com/300x450.png?text=No+Poster"

def fetch_poster(movie_title):
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"t": movie_title, "apikey": "58505b6b"},
            timeout=5
        )
        data = response.json()
        poster = data.get("Poster", "")
        if poster and poster != "N/A":
            return poster
        else:
            return FALLBACK_POSTER
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return FALLBACK_POSTER


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_index = int(movie_index)  # ✅ convert to integer
    distances = list(enumerate(similarity[movie_index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in distances:
        movie_title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_title)
        if not poster:
            poster = FALLBACK_POSTER
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
movies = movies.reset_index(drop=True)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title('Movie Recommender System')

selected_movies_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])