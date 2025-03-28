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

# Set page configuration
st.set_page_config(
    page_title="Movie Title Search",
    page_icon="🎬",
    layout="centered"
)
# App header
st.title("🎬 Movie Search Engine")
st.subheader("Find movies by describing what you can remember")

# Description
st.markdown("""
Write in plain words the key elements you can remind of the movie.
""")

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

# Footer
st.markdown("---")
st.markdown(
    "This is a semantic movie search engine that helps you find movies "
    "based on plot descriptions. It uses natural language processing to understand "
    "your query and find the most relevant matches."
)
