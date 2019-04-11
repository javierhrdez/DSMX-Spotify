import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import json
import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

from colorama import init, Fore, Back, Style
init()

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'

print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

df_songs = pd.DataFrame(columns=['AUTOR','TITULO','LETRA']) 
def get_lyrics(df, artist):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + TOKEN}
    search_url = base_url + '/search'
    AUTOR = artist
    data = {'q': AUTOR}
    response = requests.get(search_url, data=data, headers=headers)
    response = json.loads(response.content)
    hits = response.get('response').get('hits')


    for hit in hits:
        print("=" * 100)
        response = requests.get(base_url + hit.get('result').get('api_path'), headers=headers)
        response = json.loads(response.content)
        TITULO = hit.get('result').get('full_title')
        url_cancion = response.get('response').get('song').get('url')
        page = requests.get(url_cancion)
        html1 = BeautifulSoup(page.text,"html.parser") # Extract the page's HTML as a string
        LYRICS = html1.find("div", class_="lyrics").get_text()
        #LYRICS = LYRICS.replace("\n", " ") # convierte saltos de linea a espacios
        #LYRICS = re.sub(r'\[[^]]*\]', '',LYRICS) # remueve texto entre brackets []
        LYRICS = LYRICS.lower() # convierte todo a minúsculas

        #https://www.dummies.com/programming/python/how-to-search-within-a-string-in-python/ 
        shunks = LYRICS.split('\n')
        processed = []
        for shunk in shunks:
            if(shunk.startswith("letra de")):
                pass
            elif(shunk.startswith("[")):
                pass
            elif(len(shunk)==0):
                pass
            else:
                processed.append(shunk)
        LYRICS = " ".join(processed)

        print(Fore.GREEN ,shunks)
        print(Style.RESET_ALL)
        #LYRICS = " ".join(LYRICS.split())
        #LYRICS = re.sub(r'\([^)]*\)', '', LYRICS) # remueve texto entre parenteis []
        print(Fore.RED + LYRICS)
        print(Style.RESET_ALL)
        df = df.append({'AUTOR':AUTOR, 'TITULO':TITULO,'LETRA':LYRICS}, ignore_index=True)
    return df

artists = ['Juan Gabriel','Maluma', 'José José','Luis Miguel','Shakira','Ozuna','Ricardo Arjona',
        'J Balvin','Enrique Iglesias','Julieta Venegas','Alejandro Fernandez','Natalia Lafourcade',
        'Cafe Tacvba','Paulina Rubio','Gloria Trevi','Los Tigres de Norte','Silvio Rodríguez','Víctor Jara',
        'Violeta Parra','Banda Sinaloense MS de Sergio Lizárraga','La Arrolladora Banda El Limón De René Camacho']
for artist in artists:
    df_songs = get_lyrics(df_songs, artist)
df_songs.to_csv('canciones2.csv')


