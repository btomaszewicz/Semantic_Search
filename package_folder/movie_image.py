import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from package_folder.semantic_search import Movie

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')  # Replace with your TMDb API key

# def get_movie_poster(title):
#     """Fetches the movie poster URL from TMDb given a movie title."""
#     url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
#     response = requests.get(url).json()

#     if response.get("results"):
#         poster_path = response["results"][0].get("poster_path")
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"  # High-quality image URL

#     return None  # No image found

#Function to extract IMDb ID from Wikipedia
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
