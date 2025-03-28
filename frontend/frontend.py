# create a streamlit app that allows users to search movies by plot

import streamlit as st
import requests
import os

api_url = os.getenv('API_URL', 'http://localhost:8000')

def search_movies(search_term: str, page: int=1, per_page: int=10) -> list[dict]:
    response = requests.get(api_url, params={'search_term': search_term, 'page': page, 'per_page': per_page})
    return response.json()

page = 1
per_page = 10

st.title('Movie Search Engine')

movies = []

search_term = st.text_input('Enter a search term')
if st.button('Search'):
    movies = search_movies(search_term, page, per_page)
    for movie in movies:
        st.write(f"Title: {movie['title']}")
        st.write(f"Release Year: {movie['release_year']}")
        st.write(f"Director: {movie['director']}")
        st.write(f"Genre: {movie['genre']}")
        st.write(f"Wiki Page: {movie['wiki_page']}")
        st.write('---')

    if movies and st.button('Next Page', key='next_page'):
        page += 1
        movies = search_movies(search_term, page, per_page)

    if movies and page > 1 and st.button('Previous Page', key='previous_page'):
        page -= 1
        movies = search_movies(search_term, page, per_page)
