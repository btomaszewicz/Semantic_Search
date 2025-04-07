from fastapi import FastAPI, HTTPException
from .data_models import Movie
from .semantic_search import search_similar_movies
from .movie import get_imdb_from_wikipedia, get_movie_poster
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api_file:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get('/')
def root(search_term: str, page: int = 1, per_page: int = 10) -> list[Movie]:
    if not search_term:
        raise HTTPException(status_code=400, detail="Search term is required")

    try:
        movies = search_similar_movies(search_term, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Vérification si la liste est vide
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")

    return movies
