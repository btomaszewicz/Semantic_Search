# create a streamlit app that allows users to search movies by plot

import streamlit as st
import pandas as pd
from package_folder.semantic_search import search_similar_movies


# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'has_results' not in st.session_state:
    st.session_state.has_results = False

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
        height=50
    )
    if st.form_submit_button(label="Search Movies"):
        # Reset page on new search
        st.session_state.page = 1
        st.session_state.query = query
        st.session_state.has_results = True

# If we have a query (either from form submission or previous state)
if st.session_state.has_results:
    # Get movies for the current page
    movies = search_similar_movies(st.session_state.query, page=st.session_state.page, per_page=per_page)

    # Display results
    if movies:
        for movie in movies:
            st.write(f"Title: **{movie.title}**")
            st.write(f"Release Year: {movie.release_year}")
            st.write(f"Director: {movie.director}")
            st.write(f"Genre: {movie.genre}")
            st.write(f"Wiki Page: {movie.wiki_page}")
            st.write('---')

        # Add prompt and buttons for more results
        st.write("Do you see the movie you had in mind in the list?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("No, show me more movies"):
                load_more_results()
                st.experimental_rerun()
        with col2:
            if st.button("Yes, I found it"):
                st.success("Great! We're glad you found what you were looking for.")
    else:
        st.write("No more results found.")
