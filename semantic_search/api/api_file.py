from fastapi import FastAPI
import pickle
from movie_search import search_movies

app = FastAPI()

@app.get('/')
def root():
    return {'hello': 'world'}

@app.get('/predict')
def predict(search_terms):

    prediction = search_movies(search_terms)

    return {"prediction": prediction}
