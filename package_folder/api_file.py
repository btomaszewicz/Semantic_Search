from fastapi import FastAPI
import pickle

app = FastAPI()

@app.get('/')
def root():
    return {'hello': 'world'}
