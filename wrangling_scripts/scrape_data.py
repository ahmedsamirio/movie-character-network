import json
import os
import pickle
import string
import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote

BASE_URL = 'http://www.imsdb.com'
SCRIPTS_DIR = 'data'
MOVIES = 'movies.pkl'

def clean_script(text):
    """Function to clean scraped html script"""
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
                        </b>if (window!= top)
                        top.location.href=location.href
                        <b>// -->
                        </b>
                        ''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
                                  Formatting by http://simplyscripts.home.att.net
                        ''', '')
    return text.replace(r'\r', '')


def get_clean_title(name):
    """Function to return a clean movie title."""
    # remove " Script.html" from the end of the title
    name = name[:-12]

    # correct movie with format "Movie, The" to "The Movie"
    if ', The' in name:
        name = 'The ' + name.replace(', The', '')

    # escape single quotes
    name = name.replace("'", r"")
    return name



def get_script(relative_link):
    search_title = relative_link.split('/')[-1]
    clean_title = get_clean_title(search_title)
    print('fetching %s' % clean_title)
    script_front_url = BASE_URL + quote(relative_link)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")

    try:
        script_link = front_soup.find_all('p', align="center")[0].a['href']
    except IndexError:
        print('%s has no script :(' % clean_title)
        return None, None, None

    if script_link.endswith('.html'):
        save_title = script_link.split('/')[-1].split(' Script')[0]
        script_url = BASE_URL + script_link
        script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
        script_text = script_soup.find_all('td', {'class': "scrtext"})[0].get_text()
        script_text = clean_script(script_text)
        return clean_title, save_title, script_text
    else:
        print('%s is a pdf :(' % search_title)
        return None, None, None



if __name__ == "__main__":
    response = requests.get('https://imsdb.com/all-scripts.html')
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all('p')

    movies_files = {}

    for p in paragraphs:
        relative_link = p.a['href']
        search_title, save_title, script = get_script(relative_link)
        if not script:
            continue

        # clean save title from any punctuations that prevent creating a filename
        save_title = save_title[:-5].translate(str.maketrans('', '', string.punctuation)) + '.txt'
        script_file = os.path.join(SCRIPTS_DIR, save_title)

        # save script text
        with open(script_file, 'w', encoding='utf-8') as outfile:
            outfile.write(script)

        # save mapping of movie name with script text file
        movies_files[search_title] = script_file

    # save mapping to a picke file for easy loading
    movies_files_pkl =  open(os.path.join(SCRIPTS_DIR, MOVIES), 'wb')
    pickle.dump(movies_files, movies_files_pkl)
