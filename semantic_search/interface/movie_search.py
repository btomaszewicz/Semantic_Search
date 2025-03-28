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

def search_similar_movies(search_term,csv_file):

    df_movies = tokenize_csv('raw_data/wiki_movie_plots_deduped.csv', 'preprocessed_data/movies_with_tokenized_plots.csv')
    print("df_movies:", df_movies.head())  # Debug



    # Load the tokenized data
    df_movies = load_tokenized_csv('preprocessed_data/movies_with_tokenized_plots.csv',chunksize=100)
    df_movies = pd.concat(df_movies, ignore_index=True)
    print(f'df movie loaded')
    print(df_movies.head())

    # # Load the dictionary
    # dict = dictionary(df_movies['wiki_plot_tokenized'])

    # # Load the corpus
    # corp = corpus(df_movies['wiki_plot_tokenized'], dict)

    # # Load the TF-IDF model
    # movie_tfidf_model = tfidf_model(corp, dict)

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

    # Create a corpus in chunks (streaming)
    # corpus = (dictionary.doc2bow(text) for chunk in load_tokenized_csv(csv_file) for text in chunk['wiki_plot_tokenized'])

    # # Load the LSI model
    # movie_lsi_model = lsi_model(corp, dictionary, movie_tfidf_model)

    # # Load the movie index
    # movie_index(movie_lsi_model, len(dictionary))

    # Tokenize the search term and convert to LSI space



    # Get the similarity scores
    sims = movie_index[query_lsi]
    print(type(sims))
    print(sims)
    movies_list = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

    # # Check if the tokenized file exists, if not create it
    # if not os.path.exists('preprocessed_data/movies_with_tokenized_plots.csv'):
    #     print("Tokenizing raw data...")
    #     tokenize_csv('raw_data/wiki_movie_plots_deduped.csv', 'preprocessed_data/movies_with_tokenized_plots.csv')

    # # Load the data in chunks and process incrementally
    # chunks_generator = load_tokenized_csv_in_chunks('preprocessed_data/movies_with_tokenized_plots.csv', chunk_size)

    # # Initialize empty containers
    # all_tokens = []
    # all_movies = []
    # chunk_count = 0

    # # First pass: collect tokenized plots and build dictionary
    # print("Processing data in chunks and building dictionary...")
    # for chunk in chunks_generator:
    #     if chunk is None:
    #         return None

    #     chunk_count += 1
    #     print(f"Processing chunk {chunk_count} for dictionary building...")

    #     # Store movie data
    #     for _, movie in chunk.iterrows():
    #         all_movies.append({
    #             'Title': movie['Title'],
    #             'Plot': movie['Plot'],
    #             'tokens': movie['wiki_plot_tokenized']
    #         })
    #         all_tokens.append(movie['wiki_plot_tokenized'])

    #     # Process in smaller batches to avoid memory issues
    #     if chunk_count % 10 == 0:
    #         print(f"Processed {len(all_movies)} movies so far...")

    # # Now build the models with the collected data
    # print("Building models...")
    # dictionary = gensim.corpora.Dictionary(all_tokens)
    # corpus = [dictionary.doc2bow(text) for text in all_tokens]

    # # Release memory by deleting the tokens list
    # del all_tokens

    # # Build TF-IDF model
    # tfidf_model = gensim.models.TfidfModel(corpus)
    # corpus_tfidf = tfidf_model[corpus]

    # # Build LSI model (with fewer topics to save memory)
    # lsi_model = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
    # corpus_lsi = lsi_model[corpus_tfidf]

    # # Build similarity index
    # index = gensim.similarities.MatrixSimilarity(corpus_lsi)

    # # Process the query
    # query_bow = dictionary.doc2bow(tokenizer(search_term))
    # query_tfidf = tfidf_model[query_bow]
    # query_lsi = lsi_model[query_tfidf]

    # # Calculate similarities
    # similarities = index[query_lsi]

    # # Create a list of (index, similarity) tuples and sort by similarity
    # movies_list = [(i, similarity) for i, similarity in enumerate(similarities)]
    # movies_list.sort(key=lambda x: x[1], reverse=True)

    # # Rest of your search results display code...

    # Display search results
    # results_per_page = 10
    # start_index = 0


    # while start_index < len(movies_list):
    #     movie_names = []

    #     # Store original movie data for later full plot display
    #     current_page_movies = []

    #     for j, movie in enumerate(movies_list[start_index:start_index + results_per_page]):
    #         movie_index_in_df = movie[0]
    #         movie_title = df_movies['Title'][movie_index_in_df]
    #         movie_plot = df_movies['Plot'][movie_index_in_df]

    #         movie_names.append({
    #             'Index': j,  # Add display index for selection
    #             'Relevance': round((movie[1] * 100), 2),
    #             'Movie Title': movie_title,
    #             'Movie Plot': truncate_plot(movie_plot)
    #         })

    #         # Store complete information
    #         current_page_movies.append({
    #             'Index': movie_index_in_df,
    #             'Title': movie_title,
    #             'Plot': movie_plot,
    #             'Relevance': round((movie[1] * 100), 2)
    #         })

    #     results_df = pd.DataFrame(movie_names, columns=['Index', 'Relevance', 'Movie Title', 'Movie Plot'])

    #     # Set display options
    #     pd.set_option('display.max_colwidth', None)  # Don't truncate column contents
    #     pd.set_option('display.expand_frame_repr', False)  # Try to show all columns in one row
    #     pd.set_option('display.max_rows', 10)  # Show only 10 rows max
    #     pd.set_option('display.precision', 2)  # Show 2 decimal places for floats
    #     pd.set_option('display.colheader_justify', 'left')  # Left-align column headers



    #     print("\n" + "="*80)
    #     print(f"SEARCH RESULTS FOR: '{search_term}' (Page {start_index//results_per_page + 1})")
    #     print("="*80)

    #     # styled_df = results_df.style.background_gradient(
    #     # subset=['Relevance'], cmap='Blues', high=0.5
    #     # ).set_properties(**{'text-align': 'left'})
    #     print(df_movies)

    #     # Ask user if they found the movie or want to see full plot
    #     user_input = input("\nDid you find the movie you were looking for? (yes/no) or enter a movie index number to see full plot: ").strip().lower()

    #     # Check if user entered a number
    #     try:
    #         movie_idx = int(user_input)
    #         if 0 <= movie_idx < len(current_page_movies):
    #             # Display full details for the selected movie
    #             selected_movie = current_page_movies[movie_idx]
    #             print("\n" + "="*80)
    #             print(f"FULL DETAILS FOR: {selected_movie['Title']}")
    #             print(f"Relevance Score: {selected_movie['Relevance']}%")
    #             print("="*80)
    #             print("\nPLOT SUMMARY:")
    #             print(selected_movie['Plot'])
    #             print("\n" + "="*80)

    #             # Ask if they want to continue searching or return this movie
    #             continue_input = input("\nIs this the movie you were looking for? (yes/no): ").strip().lower()
    #             if continue_input == 'yes':
    #                 selected_movie['Relevance'] = f"{selected_movie['Relevance']:.2f}%"
    #                 return pd.DataFrame([selected_movie],columns=['Index', 'Relevance', 'Title', 'Plot'])
    #             # If no, continue with the loop and show the same page again
    #             continue
    #         else:
    #             print("Invalid movie index. Please try again.")
    #             continue
    #     except ValueError:
    #         # Not a number, process as yes/no
    #         pass

    #     if user_input == 'yes':
    #         # Ask which movie they want to return
    #         while True:
    #             try:
    #                 selection = int(input("Enter the index of the movie you want to select: "))
    #                 if 0 <= selection < len(current_page_movies):
    #                     return pd.DataFrame([current_page_movies[selection]])
    #                 else:
    #                     print("Invalid index. Please try again.")
    #             except ValueError:
    #                 print("Please enter a valid number.")
    #     elif user_input == 'no':

    #         results_per_page += 5
    #     else:
    #         print("Invalid input. Please enter 'yes', 'no', or a movie index.")

    # print("No more results found.")
    # return None



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
