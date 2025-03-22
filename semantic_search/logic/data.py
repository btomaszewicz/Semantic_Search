
import os
import ast
import pandas as pd
from semantic_search.logic.preprocessing import tokenizer
import ipdb


def tokenize_csv(input_csv, output_csv):

    # Check if the output CSV already exists
    input = input_csv
    out = output_csv
    # ipdb.set_trace()
    print('enter tokenize')
    if os.path.exists(output_csv):

        print(f'{output_csv} already exists. Skipping tokenization.')
        return pd.read_csv(output_csv)
    else:
        # Read the input CSV
        df_movies = pd.read_csv(input_csv)

        # Check if the 'plot' column exists
        if 'plot' in df_movies.columns:
            # Apply the tokenizer to the 'plot' column
            df_movies['wiki_plot_tokenized'] = df_movies['plot'].astype(str).apply(tokenizer)
            # Save the tokenized data to the output CSV
            df_movies.to_csv(output_csv, index=False)
            print(f'Tokenized CSV saved to {output_csv}')
            return df_movies
        else:
            print('No "plot" column found in CSV.')


def load_tokenized_csv(csv_file):

    try:
        df_movies = pd.read_csv(csv_file)
        df_movies['wiki_plot_tokenized'] = df_movies['wiki_plot_tokenized'].apply(ast.literal_eval)
        print(f'Loaded tokenized CSV from {csv_file}')
        return df_movies
    except FileNotFoundError:
        print(f'File {csv_file} not found.')
        return None

# #load the data
# df_movies = pd.read_csv('../raw_data/wiki_movie_plots_deduped.csv')

# #use the function to tokenize the plot
# df_movies['wiki_plot_tokenized'] = df_movies['Plot'].map(lambda x: tokenizer(x))

# # Save the DataFrame as a CSV file in the raw_data folder
# df_movies.to_csv('../raw_data/movies_with_tokenized_plots.csv', index=False)

# # Load the DataFrame from the CSV file
# df_movies = pd.read_csv('../raw_data/movies_with_tokenized_plots.csv')

# # Convert the string representation of lists back into actual lists of tokens
# df_movies['wiki_plot_tokenized'] = df_movies['wiki_plot_tokenized'].apply(ast.literal_eval)
