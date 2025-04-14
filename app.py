import streamlit as st
import pickle
import requests
import gdown
import os
import pandas as pd
@st.cache_resource
def fetch_poster(movie_title):
    url=f"http://www.omdbapi.com/?t={movie_title}&apikey=d074f616"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', 'https://via.placeholder.com/300x450?text=No+Poster+Found')
#load the data
movies=pickle.load(open('movies.pkl', 'rb'))
#loading similarity file
# similarity=pickle.load(open('similarity.pkl', 'rb'))
def load_similarity():
    output = 'similarity.pkl'
    if not os.path.exists(output):
        url = 'https://drive.google.com/uc?id=11fkLuNbCmTGP7dlnJLUd5zW1oSWan5V3'
        gdown.download(url, output, quiet=False, fuzzy=True, resume=True)
    with open(output, 'rb') as f:
        return pickle.load(f)

similarity = load_similarity()


movie_list=movies['title'].values

st.title('Movie Recommender System')

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    # if we sort, we will loose all the index positions
    distances = similarity[movie_index]
    movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies=[]
    recommend_posters=[]
    for i in movies_indices:
        movie_title=movies.iloc[i[0]].title
        #fetch poster from API
        recommend_posters.append(fetch_poster(movie_title))
        recommend_movies.append(movie_title)
        # print(movies_list.iloc[i[0]].title)
        # print(i[0])
    return recommend_movies, recommend_posters

#streamlit select box
selected_movie_name = st.selectbox(
    "Select a movie get recommendations:",
    movie_list
)

#on button click
if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)
    cols=st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
