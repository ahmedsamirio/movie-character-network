import os
import plotly.graph_objs as go
import pickle
from .scrape_data import SCRIPTS_DIR, MOVIES
from .text_functions import clean_script_text, sent_tokenize_script, extract_dialogues, in_top_characters
from .network_functions import get_network_traces

import pandas as pd


def return_figures(movie_file, movie_name):
    """Creates character network visualization

    Args:
        None

    Returns:
        list (dict): list containing the network

    """


    text = open(movie_file, 'r').read()
    text = clean_script_text(text)
    sents = sent_tokenize_script(text)
    dialogue = extract_dialogues(sents)
    dialogue_df = pd.DataFrame(dialogue, columns=['character', 'text'])

    # change "-" in character names to " "
    dialogue_df['character'] = dialogue_df['character'].str.replace("-", " ")
    
    # top characters lines count
    characters_lines = dialogue_df.character.value_counts()
    top_characters = characters_lines[characters_lines > 5]
    
    # Make list of dialogue exchanged
    dialogue_df['character_shifted'] = dialogue_df.character.shift(-1)
    
    # extract character pairs
    pairs = dialogue_df[['character', 'character_shifted']].values.tolist()[:-1]

    # remove dialogues from one character to themselves and sort exchanges
    pairs = ['-'.join(sorted(x)) for x in pairs if x[0] != x[1]]

    # count exchanges
    pairs = pd.Series(pairs).value_counts()
    top_pairs = pairs[in_top_characters(pairs.index, top_characters)]

    # further filter characters to inlcude only that have edges
    pair_chars = set('-'.join(top_pairs.index).split('-'))
    
    # get network trace
    edge_trace, node_trace = get_network_traces(top_characters, top_pairs, pair_chars)   
    
    traces = edge_trace + [node_trace]
    
    layout = dict(title=movie_name,
                     showlegend=False,
                     xaxis=dict(showgrid=False,
                                zeroline=False,
                                showticklabels=False),
                     yaxis=dict(showgrid=False,
                                zeroline=False,
                                showticklabels=False))

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=traces, layout=layout))

    return figures


def return_movies():
    """Function to return list of available movies."""
    movies_files_pkl = open(os.path.join(SCRIPTS_DIR, MOVIES), 'rb')
    movies_files = pickle.load(movies_files_pkl)
    movies = movies_files.keys()
    return movies


def get_movie_file(movie):
    movies_files_pkl = open(os.path.join(SCRIPTS_DIR, MOVIES), 'rb')
    movies_files = pickle.load(movies_files_pkl)
    return movies_files[movie]
