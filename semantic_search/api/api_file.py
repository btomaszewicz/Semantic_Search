from fastapi import FastAPI, Query, Response
import pandas as pd
from tabulate import tabulate
from semantic_search.interface.movie_search import search_similar_movies
from fastapi import HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}



@app.get("/search/")
def search_movies(query: str, results_per_page: int = 10, page: int = 1):
    if not query:
        return []
    return search_similar_movies(query, results_per_page, page)
