from fastapi import FastAPI
from dataclasses import Movie
from .semantic_search import search_similar_movies

app = FastAPI()

@app.get('/')
def root(search_term: str, page: int=1, per_page: int=10) -> list[Movie]:
    if not search_term:
        return []
    return search_similar_movies(search_term, page, per_page)
