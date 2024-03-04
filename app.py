import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
               'Choose a movie',
                movies['title'].values)



if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    num_recommendations = len(names)
    max_columns = 3  # Set the maximum number of columns per row

    # Calculate the number of columns based on the length of the movie names
    num_columns = min(max_columns, num_recommendations)

    for i in range(0, num_recommendations, num_columns):
        row_names = names[i:i + num_columns]
        row_posters = posters[i:i + num_columns]

        cols = st.columns(num_columns)
        for col, (name, poster) in zip(cols, zip(row_names, row_posters)):
            with col:
                st.header(name)
                st.image(poster)
