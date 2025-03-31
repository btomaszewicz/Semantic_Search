from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
from semantic_search.utils import truncate_plot
from semantic_search.logic.model import build_models
from semantic_search.logic.data import load_tokenized_csv
from semantic_search.logic.preprocessing import tokenizer
from gensim.similarities import MatrixSimilarity
from gensim.models import TfidfModel, LsiModel
from gensim.corpora import Dictionary
from tabulate import tabulate

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}



# Define the Movie response model
class Movie(BaseModel):
    index: int
    relevance: str
    title: str
    plot: str
    release_year: int
    director: str
    genre: str

# Define the Search request model
class SearchRequest(BaseModel):
    search_term: str
    page: int = 1
    results_per_page: int = 10

# Load the pre-built models
def load_models():
    model_dir = os.path.join("models")
    dictionary = Dictionary.load(os.path.join(model_dir, "movie_dictionary.dict"))
    movie_tfidf_model = TfidfModel.load(os.path.join(model_dir, "tfidf_model.tfidf"))
    movie_lsi_model = LsiModel.load(os.path.join(model_dir, "lsi_model.lsi"))
    return dictionary, movie_tfidf_model, movie_lsi_model

# Load the tokenized movie data
df_movies = load_tokenized_csv('preprocessed_data/movies_with_tokenized_plots.csv', chunksize=100)
df_movies = pd.concat(df_movies, ignore_index=True)

# Build models
dictionary, movie_tfidf_model, movie_lsi_model = build_models('preprocessed_data/movies_with_tokenized_plots.csv')
corpus_tfidf = []
for text in df_movies['wiki_plot_tokenized']:
    bow = dictionary.doc2bow(text)
    corpus_tfidf.append(list(movie_tfidf_model[bow]))
corpus_lsi = movie_lsi_model[corpus_tfidf]
movie_index = MatrixSimilarity(corpus_lsi, num_features=2000)

from sentence_transformers import SentenceTransformer, util

# Load the transformer model for reranking
rerank_model = SentenceTransformer("msmarco-MiniLM-L-6-v3")

@app.post("/search/")
async def search_movies(request: SearchRequest):
    search_term = request.search_term
    page = request.page
    results_per_page = request.results_per_page

    # Stage 1: LSI Retrieval (Retrieve Top 50 Candidates)
    query_bow = dictionary.doc2bow(search_term.lower().split())
    query_tfidf = movie_tfidf_model[query_bow]
    query_lsi = movie_lsi_model[query_tfidf]
    sims = movie_index[query_lsi]
    initial_results = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:50]  # Top 50 candidates

    # Encode query and documents with BERT
    query_embedding = rerank_model.encode(search_term, convert_to_tensor=True)
    doc_embeddings = rerank_model.encode([df_movies["Plot"].iloc[i[0]] for i in initial_results], convert_to_tensor=True)

    # Compute cosine similarity between query and documents
    rerank_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0].cpu().numpy()

    # Re-sort the results using BERT scores
    reranked_results = sorted(zip(initial_results, rerank_scores), key=lambda x: x[1], reverse=True)

    # Pagination
    start_index = (page - 1) * results_per_page
    end_index = start_index + results_per_page
    final_results = reranked_results[start_index:end_index]

    # Format response
    movie_list = []
    for j, ((movie_index_in_df, _), score) in enumerate(final_results):
        movie_list.append(Movie(
            index=j,
            relevance=f"{round(score * 100, 2)}%",
            title=df_movies["Title"].iloc[movie_index_in_df],
            plot=truncate_plot(df_movies["Plot"].iloc[movie_index_in_df]),
            release_year=df_movies["Release Year"].iloc[movie_index_in_df],
            director=df_movies["Director"].iloc[movie_index_in_df],
            genre=df_movies["Genre"].iloc[movie_index_in_df],
        ))

    return {"results": movie_list, "page": page}
