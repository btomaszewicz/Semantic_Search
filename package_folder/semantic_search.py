from pathlib import Path
import pandas as pd
import re
import string
import spacy

from gensim import corpora, models
from gensim.similarities import MatrixSimilarity

from .dataclasses import Movie

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


# Tokenizer function for the user query
from spacy.lang.en.stop_words import STOP_WORDS

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



# Search function to get the most similar movies
from operator import itemgetter

def search_similar_movies(search_term, page=1, per_page=10):

    query_bow = am_dictionary.doc2bow(tokenizer(search_term))
    query_tfidf = movie_tfidf_am_model[query_bow]
    query_lsi = movie_lsi_am_model[query_tfidf]

    am_movie_index.num_best = 100

    movies_list = am_movie_index[query_lsi]

    movies_list.sort(key=itemgetter(1), reverse=True)

    return [
        Movie(
            title=am_titles['Title'][movie[0]],
            release_year=am_titles['Release Year'][movie[0]],
            director=am_titles['Director'][movie[0]],
            genre=am_titles['Genre'][movie[0]],
            wiki_page=am_titles['Wiki Page'][movie[0]]
        ) for movie in movies_list[(page-1)*per_page:page*per_page]]
