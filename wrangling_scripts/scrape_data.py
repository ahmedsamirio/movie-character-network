import json
import os
import pickle
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


def get_script(relative_link):
    search_title = relative_link.split('/')[-1]
    print('fetching %s' % search_title)
    script_front_url = BASE_URL + quote(relative_link)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")

    try:
        script_link = front_soup.find_all('p', align="center")[0].a['href']
    except IndexError:
        print('%s has no script :(' % search_title)
        return None, None, None

    if script_link.endswith('.html'):
        save_title = script_link.split('/')[-1].split(' Script')[0]
        script_url = BASE_URL + script_link
        script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
        script_text = script_soup.find_all('td', {'class': "scrtext"})[0].get_text()
        script_text = clean_script(script_text)
        return search_title.rstrip(' Script.html'), save_title, script_text
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

        script_file = os.path.join(SCRIPTS_DIR, save_title.strip('.html') + '.txt')

        # save script text
        with open(script_file, 'w', encoding='utf-8') as outfile:
            outfile.write(script)

        # save mapping of movie name with script text file
        movies_files[search_title] = script_file

    # save mapping to a picke file for easy loading
    movies_files_pkl =  open(os.path.join(SCRIPTS_DIR, MOVIES), 'wb')
    pickle.dump(movies_files, movies_files_pkl)
