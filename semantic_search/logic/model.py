import gensim

# from gensim import corpora
from gensim.similarities import MatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

from semantic_search.logic.data import load_tokenized_csv
from gensim.models import TfidfModel, LsiModel

import os


# def dictionary (movie_plot):

#     dictionary = corpora.Dictionary(movie_plot)

#     # Filter out words that occur less than 4 documents, or more than 20% of the documents.
#     dictionary.filter_extremes(no_below=4, no_above=0.2)

#     stoplist = set('hello and if this can would should could tell ask stop come go movie film'.split())
#     stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
#     dictionary.filter_tokens(stop_ids)
#     return dictionary

# def corpus (movie_plot, dictionary):

#     corpus = [dictionary.doc2bow(desc) for desc in movie_plot]
#     return corpus


# def tfidf_model (corpus, dictionary):
#     #create the TF-IDF model
#     movie_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
#     return movie_tfidf_model

def build_models(csv_file, chunksize=100, num_topics=200):
    """Builds or loads the dictionary, TF-IDF, and LSI models."""

    model_dir = os.path.join("models")
    # File paths
    dict_path = os.path.join(model_dir, "movie_dictionary.dict")
    tfidf_path = os.path.join(model_dir, "tfidf_model.tfidf")
    lsi_path = os.path.join(model_dir, "lsi_model.lsi")

    print("Current working directory:", os.getcwd())
    # Load existing models if they exist
    if os.path.exists(dict_path) and os.path.exists(tfidf_path) and os.path.exists(lsi_path):
        print("Models already exist. Loading from disk...")
        dictionary = Dictionary.load(dict_path)
        movie_tfidf_model = TfidfModel.load(tfidf_path)
        movie_lsi_model = LsiModel.load(lsi_path)
        return dictionary, movie_tfidf_model, movie_lsi_model
    else:
        print("Generating models...")

    # Initialize empty dictionary and corpus
    dictionary = Dictionary()
    corpus = []

    # Load tokenized CSV in chunks
    for chunk in load_tokenized_csv(csv_file, chunksize):
        dictionary.add_documents(chunk['wiki_plot_tokenized'])
        corpus.extend(dictionary.doc2bow(text) for text in chunk['wiki_plot_tokenized'])

    dictionary.compactify()

    # Build TF-IDF model
    movie_tfidf_model = TfidfModel(corpus, dictionary=dictionary)

    # Build LSI model
    movie_lsi_model = LsiModel(movie_tfidf_model[corpus], id2word=dictionary, num_topics=num_topics)

    # Save models
    save_path = "models"

    dictionary.save(f"{save_path}movie_dictionary.dict")
    movie_tfidf_model.save(f"{save_path}tfidf_model.tfidf")
    movie_lsi_model.save(f"{save_path}lsi_model.lsi")

    print("Models saved to disk.")

    return dictionary, movie_tfidf_model, movie_lsi_model

# def lsi_model (corpus, dictionary, movie_tfidf_model):
#     #create the LSI model with 2000 topics
#     movie_lsi_model = gensim.models.LsiModel(movie_tfidf_model[corpus], id2word=dictionary, num_topics=2000)
#     movie_lsi_model.save("lsi_model.lsi")  # Save the trained model
#     print("LSI Model trained and saved successfully.")
#     return movie_lsi_model

def movie_index (movie_lsi_corpus, num_terms):
    # Number of terms in the TF-IDF model
    num_terms = len(dictionary)

    movie_index = MatrixSimilarity(movie_lsi_corpus, num_features = num_terms)
    return movie_index



# # Transform the TF-IDF corpus into the LSI space
# movie_lsi_corpus = movie_lsi_model[movie_tfidf_model[corpus]]

# # Transform the original BoW corpus into the TF-IDF space
# movie_tfidf_corpus = movie_tfidf_model[corpus]

# # #Serialize and Store the corpus locally for easy retrival whenever required.
# gensim.corpora.MmCorpus.serialize('movie_tfidf_model_mm', movie_tfidf_model[corpus])
# gensim.corpora.MmCorpus.serialize('movie_lsi_model_mm',movie_lsi_model[movie_tfidf_model[corpus]])

# #Load the indexed corpus
# movie_tfidf_corpus = gensim.corpora.MmCorpus('movie_tfidf_model_mm')
# movie_lsi_corpus = gensim.corpora.MmCorpus('movie_lsi_model_mm')
