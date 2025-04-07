# create a streamlit app that allows users to search movies by plot

# import streamlit as st
# import pandas as pd
# from package_folder.semantic_search import search_similar_movies


# # Initialize session state for pagination
# if 'page' not in st.session_state:
#     st.session_state.page = 1
# if 'query' not in st.session_state:
#     st.session_state.query = ""
# if 'has_results' not in st.session_state:
#     st.session_state.has_results = False

# per_page = 10

# # Function to load more results
# def load_more_results():
#     st.session_state.page += 1

# # Set page configuration
# st.set_page_config(
#     page_title="Movie Title Search",
#     page_icon="🎬",
#     layout="centered"
# )

# # App header
# st.title("🎬 Movie Title Search")
# st.subheader("Find movie titles by describing their plots")

# # Search input
# with st.form(key="search_form"):
#     query = st.text_area(
#         "Describe the plot or themes you're interested in:",
#         placeholder="Example: Dinosaur adventure. Scientists escaping genetically engineered dinosaurs on an island.",
#         height=50
#     )
#     if st.form_submit_button(label="Search Movies"):
#         # Reset page on new search
#         st.session_state.page = 1
#         st.session_state.query = query
#         st.session_state.has_results = True

# # If we have a query (either from form submission or previous state)
# if st.session_state.has_results:
#     # Get movies for the current page
#     movies = search_similar_movies(st.session_state.query, page=st.session_state.page, per_page=per_page)

#     # Display results
#     if movies:
#         for movie in movies:
#             st.write(f"Title: **{movie.title}**")
#             st.write(f"Release Year: {movie.release_year}")
#             st.write(f"Director: {movie.director}")
#             st.write(f"Genre: {movie.genre}")
#             st.write(f"Wiki Page: {movie.wiki_page}")
#             st.write('---')

#         # Add prompt and buttons for more results
#         st.write("Do you see the movie you had in mind in the list?")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("No, show me more movies"):
#                 load_more_results()
#                 st.experimental_rerun()
#         with col2:
#             if st.button("Yes, I found it"):
#                 st.success("Great! We're glad you found what you were looking for.")
#     else:
#         st.write("No more results found.")

# import streamlit as st
# import pandas as pd
# import requests
# import os
# from dotenv import load_dotenv
# from package_folder.semantic_search import search_similar_movies

# # Load environment variables
# load_dotenv()
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# # Initialize session state for pagination
# if 'page' not in st.session_state:
#     st.session_state.page = 1
# if 'query' not in st.session_state:
#     st.session_state.query = ""
# if 'has_results' not in st.session_state:
#     st.session_state.has_results = False

# per_page = 10

# # Function to get movie poster from TMDb
# def get_movie_poster(title):
#     url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
#     response = requests.get(url).json()

#     if response.get("results"):
#         poster_path = response["results"][0].get("poster_path")
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"

#     return None  # No image found

# # Function to load more results
# def load_more_results():
#     st.session_state.page += 1

# # Set page configuration
# st.set_page_config(
#     page_title="Movie Title Search",
#     page_icon="🎬",
#     layout="centered"
# )

# # App header
# st.title("🎬 Movie Title Search")
# st.subheader("Find movie titles by describing their plots")

# # Search input
# with st.form(key="search_form"):
#     query = st.text_area(
#         "Describe the plot or themes you're interested in:",
#         placeholder="Example: Dinosaur adventure. Scientists escaping genetically engineered dinosaurs on an island.",
#         height=50
#     )
#     if st.form_submit_button(label="Search Movies"):
#         # Reset page on new search
#         st.session_state.page = 1
#         st.session_state.query = query
#         st.session_state.has_results = True

# # If we have a query (either from form submission or previous state)
# if st.session_state.has_results:
#     # Get movies for the current page
#     movies = search_similar_movies(st.session_state.query, page=st.session_state.page, per_page=per_page)

#     # Display results
#     if movies:
#         for movie in movies:
#             # Get the movie poster
#             movie.image_url = get_movie_poster(movie.title)

#             col1, col2 = st.columns([1, 3])  # Layout: image on the left, text on the right

#             with col1:
#                 if movie.image_url:
#                     st.image(movie.image_url, width=120)  # Display poster
#                 else:
#                     st.write("🎬 No Image Available")  # Placeholder if no image found

#             with col2:
#                 st.write(f"**Title:** {movie.title}")
#                 st.write(f"**Release Year:** {movie.release_year}")
#                 st.write(f"**Director:** {movie.director}")
#                 st.write(f"**Genre:** {movie.genre}")
#                 st.write(f"[Wiki Page]({movie.wiki_page})")

#             st.write('---')  # Divider

#         # Add prompt and buttons for more results
#         st.write("Do you see the movie you had in mind in the list?")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("No, show me more movies"):
#                 load_more_results()
#                 st.experimental_rerun()
#         with col2:
#             if st.button("Yes, I found it"):
#                 st.success("Great! We're glad you found what you were looking for.")
#     else:
#         st.write("No more results found.")

import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from package_folder.semantic_search import search_similar_movies
from movie_image import get_movie_poster, get_imdb_from_wikipedia
import logging

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'has_results' not in st.session_state:
    st.session_state.has_results = False
if 'director' not in st.session_state:
    st.session_state.director = ""
if 'cast' not in st.session_state:
    st.session_state.cast = ""  # Initialize 'cast' as an empty string

per_page = 10

# Function to load more results
def load_more_results():
    st.session_state.page += 1

# Set page configuration
st.set_page_config(
    page_title="Movie Title Search",
    page_icon="🎬",
    layout="centered"
)

# App header
st.title("🎬 Movie Title Search")
st.subheader("Find movie titles by describing their plots")

# Search input
with st.form(key="search_form"):
    query = st.text_area(
        "Describe the plot or themes you're interested in:",
        placeholder="Example: Dinosaur adventure. Scientists escaping genetically engineered dinosaurs on an island.",
        height=68)
    director = st.text_input("Optional: Filter by director name")
    cast_input = st.text_input("Optional: Filter by cast (comma-separated)")

    if st.form_submit_button(label="Search Movies"):
        # Reset page on new search
        st.session_state.page = 1
        st.session_state.query = query
        st.session_state.has_results = True

# If we have a query (either from form submission or previous state)
if st.session_state.has_results:
    # Get movies for the current page
    cast_list = [c.strip() for c in st.session_state.cast.split(",")] if st.session_state.cast else None
    movies = search_similar_movies(
    st.session_state.query,
    page=st.session_state.page,
    per_page=per_page,
    query_director=st.session_state.director,
    query_cast=cast_list
)

    # Display results
    if movies:
        for movie in movies:
            # If IMDb ID is missing, try fetching from Wikipedia
            if not hasattr(movie, 'imdb_id') or not movie.imdb_id:
                movie.imdb_id = get_imdb_from_wikipedia(movie.wiki_page)

            # Get the movie poster (uses IMDb ID first, falls back to title)
            movie.image_url = get_movie_poster(movie)

            col1, col2 = st.columns([1, 3])  # Layout: image on the left, text on the right

            with col1:
                if movie.image_url:
                    st.image(movie.image_url, width=120)  # Display poster
                else:
                    st.write("🎬 No Image Available")  # Placeholder if no image found

            with col2:
                st.write(f"**Title:** {movie.title}")
                st.write(f"**Release Year:** {movie.release_year}")
                st.write(f"**Director:** {movie.director}")
                st.write(f"**Genre:** {movie.genre}")
                st.write(f"[Wiki Page]({movie.wiki_page})")
                if movie.imdb_id:
                    st.write(f"[IMDb](https://www.imdb.com/title/{movie.imdb_id})")

            st.write('---')  # Divider

        # Add prompt and buttons for more results
        st.write("Do you see the movie you had in mind in the list?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("No, show me more movies"):
                load_more_results()
                logging.debug("Rerun triggered due to condition met")
                st.rerun()
        with col2:
            if st.button("Yes, I found it"):
                st.success("Great! We're glad you found what you were looking for.")
    else:
        st.write("No more results found.")
