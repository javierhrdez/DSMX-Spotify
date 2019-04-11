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
SPOTIFY_CLIENT_ID = '7f74cef68ab34c7594db5f51214425e8'
SPOTIFY_CLIENT_SECRET = '5b1ba739e66c4b69be576afca507e458'
JAVIER_ID = '12137393711'


#GENIUS API (EXTRACCION DE LETRAS)
GENIUS_TOKEN = '4VxBnGpiY6jTRAPPqfBuibNBufeGmOAqn5_RyDbsLWMaNg4H9okxe14NEn5iah1T'


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


df_artists = pd.DataFrame()

def get_artist(q):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    search_url = base_url + '/search'
    data = {'q': q}
    try:
        response = requests.get(search_url, data=data, headers=headers)
        response = json.loads(response.content)
        hits = response.get('response').get('hits')
        #pprint.pprint(hits)
        for hit in hits:
            artist =  hit.get('result').get('primary_artist')
            artist_id = artist['id']
            artist_name = artist['name']
            print("-->",artist_name)
            yield artist_id,artist_name
    except:
        yield 0,""





# music = pd.read_csv("top_200_unicos.csv")
# for i,row in music.iterrows():
#     try:
#         artist = row['artist']
#         #print(artist)
#         #artist_id,artist_name = get_artist(artist)
#         for  artist_id,artist_name in get_artist(artist):
#             #print(artist_name)
#             #pprint.pprint(artist)
#             print(Back.RED +"SPOTIFY ======>"+ artist_name)
#             print(Back.GREEN +"GENIUS ======>"+ artist_name.split(',')[0])
#             print(Style.RESET_ALL)
#             df_artists = df_artists.append({'artist_name':artist_name.split(',')[0], 'artist_id':artist_id }, ignore_index=True)
#     except:
#         pass
# df_artists['artist_id'] = df_artists['artist_id'].astype(int)
# df_artists.to_csv('data/genius_artists_3.csv')

for  artist_id,artist_name in get_artist('Sebastian Yatra'):
    print(artist_name)
#get_artist('Sebastian Yatra')
#get_artist('U2')