# import streamlit as st
# import os
# import requests
# from dotenv import load_dotenv
# from package_folder.semantic_search import search_similar_movies
# from package_folder.movie_image import get_movie_poster, get_imdb_from_wikipedia

# load_dotenv()

# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# response = requests.get(f"{BACKEND_URL}/search?query=movie")

# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# api_url = os.getenv('API_URL', 'http://localhost:8000')

# def search_movies(search_term: str, page: int=1, per_page: int=10) -> list[dict]:
#     response = requests.get(api_url, params={'search_term': search_term, 'page': page, 'per_page': per_page})
#     return response.json()

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
#             # If IMDb ID is missing, try fetching from Wikipedia
#             if not hasattr(movie, 'imdb_id') or not movie.imdb_id:
#                 movie.imdb_id = get_imdb_from_wikipedia(movie.wiki_page)

#             # Get the movie poster (uses IMDb ID first, falls back to title)
#             movie.image_url = get_movie_poster(movie)

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
#                 if movie.imdb_id:
#                     st.write(f"[IMDb](https://www.imdb.com/title/{movie.imdb_id})")

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
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Get backend URL from environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

def get_imdb_from_wikipedia(wiki_url):
    """Extracts IMDb ID from a Wikipedia movie page."""
    try:
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            if 'imdb.com/title/' in link['href']:
                return link['href'].split("/")[-2]  # Extract IMDb ID (e.g., tt0123456)

    except Exception as e:
        print(f"Error fetching IMDb ID: {e}")

    return None  # No IMDb ID found

        # Function to get movie poster from TMDb using IMDb ID or title
def get_movie_poster(movie):
    # If movie is a Movie object, extract the imdb_id
    if isinstance(movie, Movie):
        title = movie.title
    else:
        # If movie is just a string (title), use it directly
        title = movie


    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url).json()


    # Check if the results exist and if the poster path is available
    if response.get("results"):
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            print("No poster path found.")
    else:
        print("No results found for movie:", title)

    return None  # No image found


def search_movies(search_term: str, page: int = 1, per_page: int = 10) -> list:
    """Query the FastAPI backend to retrieve movie search results."""
    response = requests.get(
        f"{BACKEND_URL}/search",
        params={"query": search_term, "page": page, "per_page": per_page}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching movie data from backend")
        return []

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'has_results' not in st.session_state:
    st.session_state.has_results = False

per_page = 10  # Number of movies per page

def load_more_results():
    """Load the next page of results."""
    st.session_state.page += 1

# Page settings
st.set_page_config(page_title="Movie Title Search", page_icon="🎬", layout="centered")
st.title("🎬 Movie Title Search")
st.subheader("Find movie titles by describing their plots")


# Search form
with st.form(key="search_form"):
    query = st.text_area(
        "Describe the plot or themes you're interested in:",
        placeholder="Example: Dinosaur adventure. Scientists escaping genetically engineered dinosaurs on an island.",
        height=68
    )
    if st.form_submit_button(label="Search Movies"):
        st.session_state.page = 1
        st.session_state.query = query
        st.session_state.has_results = True

# If query is present, fetch results
if st.session_state.has_results:
    movies = search_movies(st.session_state.query, page=st.session_state.page, per_page=per_page)

    if movies:
        for movie in movies:
            # Try fetching IMDb ID if missing
            if not movie.get("imdb_id"):
                movie["imdb_id"] = get_imdb_from_wikipedia(movie["wiki_page"])

            # Fetch movie poster
            movie["image_url"] = get_movie_poster(movie)

            col1, col2 = st.columns([1, 3])

            with col1:
                if movie["image_url"]:
                    st.image(movie["image_url"], width=120)
                else:
                    st.write("🎬 No Image Available")

            with col2:
                st.write(f"**Title:** {movie['title']}")
                st.write(f"**Release Year:** {movie['release_year']}")
                st.write(f"**Director:** {movie['director']}")
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"[Wiki Page]({movie['wiki_page']})")
                if movie["imdb_id"]:
                    st.write(f"[IMDb](https://www.imdb.com/title/{movie['imdb_id']})")

            st.write('---')

        # Pagination
        st.write("Do you see the movie you had in mind?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("No, show me more movies"):
                load_more_results()
                st.rerun()
        with col2:
            if st.button("Yes, I found it"):
                st.success("Great! We're glad you found what you were looking for.")
    else:
        st.write("No more results found.")
