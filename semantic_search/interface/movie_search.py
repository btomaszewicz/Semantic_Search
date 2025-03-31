import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from operator import itemgetter
from semantic_search.utils import truncate_plot
from semantic_search.logic.model import movie_index,build_models
from semantic_search.logic.data import load_tokenized_csv, tokenize_csv
from semantic_search.logic.preprocessing import tokenizer


from gensim.similarities import MatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LsiModel
import os

from tabulate import tabulate
from colorama import Fore, Style

def search_similar_movies(search_term):

    df_movies = tokenize_csv('raw_data/wiki_movie_plots_deduped.csv', 'preprocessed_data/movies_with_tokenized_plots.csv')
    print("df_movies:", df_movies.head())  # Debug



    # Load the tokenized data
    df_movies = load_tokenized_csv('preprocessed_data/movies_with_tokenized_plots.csv',chunksize=100)
    df_movies = pd.concat(df_movies, ignore_index=True)
    print(f'df movie loaded')
    print(df_movies.head())


    # Définir le bon chemin du fichier CSV
    csv_path = os.path.join("preprocessed_data", "movies_with_tokenized_plots.csv")

    # Appeler build_models avec le bon chemin
    dictionary, movie_tfidf_model, movie_lsi_model = build_models(csv_path)
    print(f'3 models built')

    print("Current working directory:", os.getcwd())

    # Dossier contenant les modèles
    model_dir = os.path.join("models")

    # Chargement manuel des modèles avec le bon chemin
    dictionary = Dictionary.load(os.path.join(model_dir, "movie_dictionary.dict"))
    movie_tfidf_model = TfidfModel.load(os.path.join(model_dir, "tfidf_model.tfidf"))
    movie_lsi_model = LsiModel.load(os.path.join(model_dir, "lsi_model.lsi"))

    # Convert movie corpus into LSI space
    # Convert the generator to a list

    tokenized_plots = list(df_movies['wiki_plot_tokenized'])

# Now loop over the list
    corpus_tfidf = []
    for text in tokenized_plots:
        bow = dictionary.doc2bow(text)
        corpus_tfidf.append(list(movie_tfidf_model[bow]))
    corpus_lsi = movie_lsi_model[corpus_tfidf]
    # Create similarity index
    movie_index = MatrixSimilarity(corpus_lsi, num_features=2000)
    print(movie_index)
    # Convert search term to tokenized bow format
    query_bow = dictionary.doc2bow(search_term.lower().split())
    # query_bow = dict.doc2bow(tokenizer(search_term))
    query_tfidf = movie_tfidf_model[query_bow]
    query_lsi = movie_lsi_model[query_tfidf]


    # Get the similarity scores
    sims = movie_index[query_lsi]
    print(type(sims))
    print(sims)
    movies_list = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)


    results_per_page = 10
    start_index = 0

    while start_index < len(movies_list):
        movie_names = []
        current_page_movies = []

        for j, movie in enumerate(movies_list[start_index:start_index + results_per_page]):
            movie_index_in_df = movie[0]
            movie_title = df_movies['Title'].iloc[movie_index_in_df]
            movie_plot = df_movies['Plot'].iloc[movie_index_in_df]
            movie_year = df_movies['Release Year'].iloc[movie_index_in_df]
            movie_director = df_movies['Director'].iloc[movie_index_in_df]
            movie_genre = df_movies['Genre'].iloc[movie_index_in_df]

            movie_names.append({
                'Index': j,
                'Relevance': f"{Fore.BLUE}{round((movie[1] * 100), 2)}%{Style.RESET_ALL}",
                'Movie Title': movie_title,
                'Movie Plot': truncate_plot(movie_plot),
                'Release Year': movie_year,
                'Director': movie_director,
                'Genre': movie_genre
            })

            current_page_movies.append({
                'Index': movie_index_in_df,
                'Title': movie_title,
                'Plot': movie_plot,
                'Relevance': round((movie[1] * 100), 2),
                'Release Year': movie_year,
                'Director': movie_director,
                'Genre': movie_genre
            })

        # **Formatted table output using tabulate**
        results_table = tabulate(movie_names, headers="keys", tablefmt="fancy_grid")

        print("\n" + "═" * 90)
        print(f"🔍  SEARCH RESULTS FOR: {Fore.YELLOW}'{search_term}'{Style.RESET_ALL} (Page {start_index//results_per_page + 1})")
        print("═" * 90)
        print(results_table)

        user_input = input("\n📌 Did you find the movie you were looking for? (yes/no) or enter a movie index: ").strip().lower()

        try:
            movie_idx = int(user_input)
            if 0 <= movie_idx < len(current_page_movies):
                selected_movie = current_page_movies[movie_idx]
                print("\n" + "═" * 90)
                print(f"🎬 FULL DETAILS FOR: {Fore.GREEN}{selected_movie['Title']}{Style.RESET_ALL}")
                print(f"🔹 Relevance Score: {Fore.CYAN}{selected_movie['Relevance']}%{Style.RESET_ALL}")
                print("═" * 90)
                print("\n📖 PLOT SUMMARY:")
                print(selected_movie['Plot'])
                print("\n" + "═" * 90)

                continue_input = input("\n✅ Is this the movie you were looking for? (yes/no): ").strip().lower()
                if continue_input == 'yes':
                    return pd.DataFrame([selected_movie], columns=['Index', 'Relevance', 'Title', 'Plot'])

                continue  # If not, return to the results page

        except ValueError:
            pass  # Process as yes/no input

        if user_input == 'yes':
            while True:
                try:
                    selection = int(input("🎯 Enter the index of the movie you want to select: "))
                    if 0 <= selection < len(current_page_movies):
                        return pd.DataFrame([current_page_movies[selection]])
                    else:
                        print("⚠️ Invalid index. Please try again.")
                except ValueError:
                    print("⚠️ Please enter a valid number.")
        elif user_input == 'no':
            results_per_page += 5  # Increase results per page for next round
        else:
            print("⚠️ Invalid input. Please enter 'yes', 'no', or a movie index.")

    print("❌ No more results found.")
    return None
