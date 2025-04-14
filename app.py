import streamlit as st
import pickle
import requests
import gdown
import os

@st.cache_resource
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=d074f616"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', 'https://via.placeholder.com/300x450?text=No+Poster+Found')

# Load movie data
movies = pickle.load(open('movies.pkl', 'rb'))

# Load similarity matrix
def load_similarity():
    output = 'similarity.pkl'
    if not os.path.exists(output):
        url = 'https://drive.google.com/uc?id=11fkLuNbCmTGP7dlnJLUd5zW1oSWan5V3'
        gdown.download(url, output, quiet=False, fuzzy=True, resume=True)
    with open(output, 'rb') as f:
        return pickle.load(f)

similarity = load_similarity()

# recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movies_indices:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

st.title("🎬 Movie Recommender System")

# Movie selector
selected_movie = st.selectbox("Select a movie to get recommendations:", movies['title'].values)

# Recommend button and output
if st.button("🎥 Recommend"):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie)

    # Display recommendations with columns
    st.subheader("🎯 Top 5 Recommendations:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)

    st.balloons() 
