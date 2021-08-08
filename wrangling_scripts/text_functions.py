import nltk
import re

import numpy as np
import pandas as pd

from itertools import chain
from pdfminer.high_level import extract_text
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder


def read_pdf(pdf_path):
    """Function to read pdf file using pdfminer extract_text."""
    pdf = extract_text(pdf_path)
    return pdf


def clean_script_text(script, remove_slugs=True):
    """Function to clean script text extracted from pdf file."""
    # remove (CONT'D)
    tmp = re.sub(r'\(CONT.{1}D\)', '\n', script)
    
    # remove ()
    tmp = re.sub(r'\(.*\)', '', tmp)
    
    # remove INSERT CUT
    tmp = re.sub(r'INSERT CUT: ', '', tmp)
    
    # remove script headings
    tmp = re.sub(r'(?:INT|EXT){1}\..*\s+', '', tmp)

    # replace " \n" with spaces
    tmp = re.sub(' \n', ' ', tmp)
    
    # remove "\r"
    tmp = re.sub('\r', '', tmp)

    # remove "\x0c"
    tmp = re.sub(r'\x0c', '', tmp)
    
    return tmp


def sent_tokenize_script(script):
    # split using \n\n
    sents = script.split('\n\n')

    # further split using \n
    sents = [sent.split('\n') for sent in sents]

    # merge lists within lists
    sents = list(chain.from_iterable(sents))
    
    return sents


def extract_dialogues(script_sents):
    """Function to extract dialogues from tokenized script sentences."""
    pattern_compile = re.compile(r'[.,–!:]')
    dialogues = []
    add_dialogue = False
    for sent in script_sents:
        if not (sent.startswith('(') and sent.endswith(')')):
            if add_dialogue:
                if not (sent.strip().isupper() and not pattern_compile.search(sent)):
                    dialogues.append((character, sent))
                add_dialogue = False
            if (sent.strip().isupper() and not pattern_compile.search(sent))\
               and not (sent.strip().startswith('(') and sent.strip().endswith(')')):
                character = sent.strip()
                add_dialogue = True
    return dialogues


def most_common_words(tokens, n=10):
    """Function return series with n most common words in a text."""
    fdist = FreqDist(tokens)
    top_n = pd.Series(dict(fdist.most_common(n)))
    return top_n 


def find_collocations(tokens, n=10):
    """Function that returns a series the n highest score bigram collocations."""
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    collocations = finder.score_ngrams(bigram_measures.likelihood_ratio)[:n]
    
    # join bigrams into one str
    collocations = [('-'.join(bigrams), score) for bigrams, score in collocations]
    top_n = pd.Series(dict(collocations))  
    return top_n


def in_top_characters(pairs, top_characters):
    """Checks if character pair are in top characters."""
    mask = []
    for pair in pairs:
        pair_list = pair.split('-')
        if pair_list[0] in top_characters and pair_list[1] in top_characters:
            mask.append(True)
        else:
            mask.append(False)
    return mask
