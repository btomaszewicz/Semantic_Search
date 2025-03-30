# create a streamlit app that allows users to search movies by plot

import streamlit as st
import pandas as pd
from package_folder.semantic_search import search_similar_movies


page = 1
per_page = 10

# Set page configuration
st.set_page_config(
    page_title="Movie Title Search",
    page_icon="🎬",
    layout="centered"
)

# App header
st.title("🎬 Movie Title Search")
st.subheader("Find movie titles by describing their plots")

# # Description
# st.markdown("""
# Enter what you remember from a movie plot and we'll find the closest matches for you!
# """)

# st.markdown("---")
# st.markdown(
#     "This is a semantic search engine that helps you find movies "
#     "based on plot descriptions. It uses natural language processing to understand "
#     "your query and find the most relevant matches."
# )

# Search input
with st.form(key="search_form"):
    query = st.text_area(
        "Describe the plot or themes you're interested in:",
        placeholder="Example: Dinosaur adventure. Scientists escaping genetically engineered dinosaurs on an island.",
        height=50
    )
    if st.form_submit_button(label="Search Movies"):
        # Replace search_similar_movies_df with search_similar_movies
        movies = search_similar_movies(query, page=page, per_page=per_page)

        for movie in movies:
            st.write(f"Title: **{movie.title}**")
            st.write(f"Release Year: {movie.release_year}")
            st.write(f"Director: {movie.director}")
            st.write(f"Genre: {movie.genre}")
            st.write(f"Wiki Page: {movie.wiki_page}")
            st.write('---')
