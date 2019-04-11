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

# datos spotify
SPOTIFY_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
SPOTIFY_CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXx'
JAVIER_ID = 'XXXXXXXXXXXXXXXXXXXX'


#GENIUS API (EXTRACCION DE LETRAS)
GENIUS_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXX'


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_songs(artist_id):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    page = 1
    while(page):
        search_url = base_url + '/artists/' + str(artist_id) + '/songs?per_page=50&page=' + str(page)
        try:
            response = requests.get(search_url,  headers=headers)
            response = json.loads(response.content)
            #pprint.pprint(response)
            page = response['response']['next_page']
            songs = response['response']['songs']
            for song in songs:
                #print("*"* 100)
                song_id = song.get('id')
                song_title = song.get('title')
                song_full_title = song.get('full_title')
                song_title_with_featured = song.get('title_with_featured')
                primary_artist = song.get('primary_artist')
                primary_artist_id = primary_artist.get('id')
                primary_artist_name = primary_artist.get('name')
                if artist_id == primary_artist_id:
                    yield song_id,song_title_with_featured
        except:
            yield 0,""            

            #print(song_id,">>>>", song_title,">>>>", song_full_title + '>>>>' , song_title_with_featured)
        #print(page)
    
def get_lyrics(song_id):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    search_url = base_url + '/songs/' + str(song_id) + '?text_format=plain'
    #search_url = base_url + '/songs/' + str(song_id)
    try:
        response = requests.get(search_url, headers=headers)
        response = json.loads(response.content)
        #pprint.pprint(response)
        api_path = response['response']['song']['api_path']
        #print(api_path)
        #except:
        #    return ""
        # EXTRAE CANCION DESDE GENIUS
        response = requests.get(base_url + api_path, headers=headers)
        response = json.loads(response.content) 
        url_cancion = response.get('response').get('song').get('url')
        page = requests.get(url_cancion)
        html = BeautifulSoup(page.text,"html.parser") # Extract the page's HTML as a string
        lyrics = html.find("div", class_="lyrics").get_text()
        lyrics = lyrics.lower() # convierte todo a minúsculas
        shunks = lyrics.split('\n')
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
        lyrics = " ".join(processed)
        return lyrics
    except:
        return ""




df_catalog = pd.DataFrame()

music = pd.read_csv("data/artistas.csv")
#music = music.head()
for i,row in music.iterrows():
    try:
        artist_id = row['artist_id']
        artist_name = row['artist_name']
        print(artist_id,"-->",artist_name)
        #song_id, song_title = get_songs(artist_id)
        for song_id, song_title in get_songs(artist_id):
            print(Back.RED +"ARTIST ======>"+ artist_name)
            print(Back.GREEN +"CANCION ======>"+ song_title)
            #lyrics = get_lyrics(song_id)
            #print(Back.BLUE + lyrics)
            print(Style.RESET_ALL)
            #df_catalog = df_catalog.append({"artist_name":artist_name,"artist_id":artist_name,"song_title":song_title,"song_id": song_id,"lyrics":lyrics}, ignore_index=True)
            df_catalog = df_catalog.append({"artist_name":artist_name,"artist_id":artist_id,"song_title":song_title,"song_id": song_id}, ignore_index=True)
    except:
        pass
    time.sleep(0.5)
df_catalog['artist_id'] = df_catalog['artist_id'].astype(int)
df_catalog['song_id'] = df_catalog['song_id'].astype(int)
df_catalog.to_csv('data/genius_catalog_2.csv')

