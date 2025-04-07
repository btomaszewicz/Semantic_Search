from pathlib import Path
import pandas as pd
import re
import string
import spacy

from gensim import corpora, models
from gensim.similarities import MatrixSimilarity

from .data_models import Movie
# Search function to get the most similar movies
from operator import itemgetter
# Tokenizer function for the user query
from spacy.lang.en.stop_words import STOP_WORDS

from movie_image import get_movie_poster



#Load the Gensim dictionary for the American movies subset

base_dir = Path(__file__).resolve().parents[1]

am_dictionary = corpora.dictionary.Dictionary.load(str(base_dir / 'models' / 'am_dictionary.dict'))

#Load th TF-IDF and LSI models
movie_tfidf_am_model = models.TfidfModel.load(str(base_dir / 'models' / 'movie_tfidf_am_model'))
movie_lsi_am_model = models.LsiModel.load(str(base_dir / 'models' / 'movie_lsi_am_model'))

#Load the dataframe with titles, year, director, genre and wiki page
am_titles = pd.read_feather(str(base_dir / 'models' / 'am_titles.feather'))

#Load the indexed corpus from the transformed corpus (document-topic matrix).
movie_lsi_am_corpus = corpora.MmCorpus(str(base_dir / 'models' / 'movie_lsi_am_model_mm'))

#Load the MatrixSimilarity
am_movie_index = MatrixSimilarity(movie_lsi_am_corpus, num_features = 2000)



spacy_nlp = spacy.load('en_core_web_sm')

punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS

def tokenizer(sentence):
    sentence = re.sub('\'','',sentence)
    sentence = re.sub('\w*\d\w*','',sentence)
    sentence = re.sub(' +',' ',sentence)
    sentence = re.sub(r'\n: \'\'.*','',sentence)
    sentence = re.sub(r'\n!.*','',sentence)
    sentence = re.sub(r'^:\'\'.*','',sentence)
    sentence = re.sub(r'\n',' ',sentence)
    sentence = re.sub(r'[^\w\s]',' ',sentence)
    tokens = spacy_nlp(sentence)
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]
    return tokens



# def search_similar_movies_df(search_term, page=1, per_page=10):
#     query_bow = am_dictionary.doc2bow(tokenizer(search_term))
#     query_tfidf = movie_tfidf_am_model[query_bow]
#     query_lsi = movie_lsi_am_model[query_tfidf]

#     # Set num_best to ensure we get enough results for the requested page
#     # We could set this higher if we anticipate needing more results
#     am_movie_index.num_best = page * per_page

#     movies_list = am_movie_index[query_lsi]

#     # Sort by similarity score in descending order
#     movies_list.sort(key=itemgetter(1), reverse=True)

#     # Calculate start and end indices for the requested page
#     start_idx = (page - 1) * per_page
#     end_idx = start_idx + per_page

#     # Slice the results to get just the current page
#     page_movies_list = movies_list[start_idx:end_idx]

#     # Convert to DataFrame
#     df = pd.DataFrame([
#         {
#             'Title': am_titles['Title'][movie[0]],
#             'Release Year': am_titles['Release Year'][movie[0]],
#             'Director': am_titles['Director'][movie[0]],
#             'Genre': am_titles['Genre'][movie[0]],
#             'Wiki Page': am_titles['Wiki Page'][movie[0]],
#             'Similarity': float(movie[1])
#         } for movie in page_movies_list])

#     # Return DataFrame along with pagination metadata
#     total_results = len(movies_list)
#     total_pages = (total_results + per_page - 1) // per_page

#     pagination_info = {
#         'page': page,
#         'per_page': per_page,
#         'total_results': total_results,
#         'total_pages': total_pages
#     }

#     return df, pagination_info


def compute_metadata_score(query_director, query_cast, movie_director, movie_cast):
    score = 0.0

    # Normalize inputs
    query_director = (query_director or "").strip().lower()
    movie_director = (movie_director or "").strip().lower()
    movie_cast = (movie_cast or "")

    # Director match
    if query_director and query_director in movie_director:
        score += 1.0

    # Cast overlap
    if query_cast:
        query_cast_set = set([name.strip().lower() for name in query_cast])
        movie_cast_set = set([name.strip().lower() for name in movie_cast.split(",") if name])
        overlap = len(query_cast_set & movie_cast_set)
        score += overlap / max(len(query_cast_set), 1)

    return score

def search_similar_movies_df(search_term, page=1, per_page=10, query_director=None, query_cast=None, metadata_weight=0.2):
    query_bow = am_dictionary.doc2bow(tokenizer(search_term))
    query_tfidf = movie_tfidf_am_model[query_bow]
    query_lsi = movie_lsi_am_model[query_tfidf]

    # Temporarily grab more movies to ensure we're considering a larger set for re-ranking
    am_movie_index.num_best = 100  # Increased to ensure we get a good pool for re-ranking

    # Get raw LSI similarities
    raw_results = am_movie_index[query_lsi]

    # Store combined scores
    combined_scores = []

    # Iterate through the results and compute the combined scores
    for movie_id, lsi_score in raw_results:
        row = am_titles.iloc[movie_id]
        meta_score = compute_metadata_score(
            query_director or "",
            query_cast or [],
            row.get('Director', ''),
            row.get('Cast', '')  # Make sure 'Cast' exists in your DataFrame
        )

        total_score = lsi_score + metadata_weight * meta_score
        combined_scores.append((movie_id, total_score))

    # Debugging: Print out the combined scores before sorting
    print("Combined Scores before sorting:")
    for movie_id, score in combined_scores:
        print(f"Movie ID: {movie_id}, Score: {score}")

    # Sort all results by the combined score (higher is better)
    combined_scores.sort(key=itemgetter(1), reverse=True)

    # Debugging: Print out the combined scores after sorting
    print("Combined Scores after sorting:")
    for movie_id, score in combined_scores:
        print(f"Movie ID: {movie_id}, Score: {score}")

    # Apply pagination: calculate the start and end indices for the page
    start = (page - 1) * per_page
    end = start + per_page
    page_scores = combined_scores[start:end]

    # Create a DataFrame for the top N results
    df = pd.DataFrame([
        {
            'Title': am_titles['Title'][movie_id],
            'Release Year': am_titles['Release Year'][movie_id],
            'Director': am_titles['Director'][movie_id],
            'Genre': am_titles['Genre'][movie_id],
            'Wiki Page': am_titles['Wiki Page'][movie_id],
            'Similarity': float(score)
        } for movie_id, score in page_scores
    ])

    # Calculate total number of results and total number of pages for pagination metadata
    total_results = len(combined_scores)
    total_pages = (total_results + per_page - 1) // per_page

    return df, {'page': page, 'per_page': per_page, 'total_results': total_results, 'total_pages': total_pages}




def search_similar_movies(search_term, page=1, per_page=10, query_director=None, query_cast=None):
    movies_df, _ = search_similar_movies_df(
        search_term, page=page, per_page=per_page,
        query_director=query_director,
        query_cast=query_cast
    )
    movies_list = movies_df.to_dict(orient='records')

    return [
        Movie(
            title=movie['Title'],
            release_year=movie['Release Year'],
            director=movie['Director'],
            genre=movie['Genre'],
            wiki_page=movie['Wiki Page'],
            image_url=get_movie_poster(movie['Title']),
            imdb_id=movie.get('IMDB ID')
        ) for movie in movies_list
    ]


# def search_similar_movies(search_term, page=1, per_page=10):
#     movies_df, _ = search_similar_movies_df(search_term, page=page, per_page=per_page)
#     movies_list = movies_df.to_dict(orient='records')
#     return [
#         Movie(
#             title=movie['Title'],
#             release_year=movie['Release Year'],
#             director=movie['Director'],
#             genre=movie['Genre'],
#             wiki_page=movie['Wiki Page'],
#             image_url=get_movie_poster(movie['Title']),  # Fetch movie poster URL
#             imdb_id=movie.get('IMDB ID')  # Include IMDb ID if available
#         ) for movie in movies_list]
