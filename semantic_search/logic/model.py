import gensim

from gensim import corpora
from gensim.similarities import MatrixSimilarity

def dictionary (movie_plot):

    dictionary = corpora.Dictionary(movie_plot)

    # Filter out words that occur less than 4 documents, or more than 20% of the documents.
    dictionary.filter_extremes(no_below=4, no_above=0.2)

    stoplist = set('hello and if this can would should could tell ask stop come go movie film'.split())
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    return dictionary

def corpus (movie_plot, dictionary):

    corpus = [dictionary.doc2bow(desc) for desc in movie_plot]
    return corpus


def tfidf_model (corpus, dictionary):
    #create the TF-IDF model
    movie_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
    return movie_tfidf_model

def lsi_model (corpus, dictionary, movie_tfidf_model):
    #create the LSI model with 2000 topics
    movie_lsi_model = gensim.models.LsiModel(movie_tfidf_model[corpus], id2word=dictionary, num_topics=2000)
    return movie_lsi_model

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
