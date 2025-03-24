# create a streamlit app that allows users to search movies by plot

import streamlit as st
import pandas as pd
from package_folder.semantic_search import search_similar_movies_df


page = 1
per_page = 10

st.title('Movie Search Engine')


search_term = st.text_input('Enter a search term')
movies = search_similar_movies_df(search_term)


# Button to trigger the search
if st.button('Search'):
    # Fetch movies using the search function
    movies = search_similar_movies_df(search_term)

    # Check if movies were found
    # Display the results in a table
    st.write("Search Results:")


    # # format the frontend column Wiki Page to be clickable
    # def make_clickable(val):
    #     return f'<a href="{val}">{val}</a>'

    # movies['wiki_page'] = movies['wiki_page'].apply(make_clickable)
    st.dataframe(movies, column_config={'Wiki Page': st.column_config.LinkColumn('Wiki Page')})
