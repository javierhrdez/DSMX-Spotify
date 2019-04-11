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
SPOTIFY_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
SPOTIFY_CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
JAVIER_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#GENIUS API (EXTRACCION DE LETRAS)
GENIUS_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def show_track(track):
    artists = [artist['name'] for artist in track['artists']]
    album = track['album']
    album_name = album['name']
    #considerando solo el primer artista de la cancion
    #yield track['artists'][0]['name'],track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i
    #considerando todos los artistas de la cancion
    return ",".join(artists),track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i

def get_lyrics(song_id):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    search_url = base_url + '/songs/' + str(song_id)
    try:
        response = requests.get(search_url, headers=headers)
        response = json.loads(response.content)
        api_path = hits = response.get('response').get('song').get('api_path')
        print(api_path)
        #pprint.pprint(response)

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


db = pd.DataFrame()
song = pd.read_csv("data/genius_catalog_end.csv")
for i,row in song.iterrows():
    try:
        #artist_id,artist_name,song_id,song_title,url
        genius_song_id = row['song_id']
        genius_song_title = row['song_title']
        genius_artist_id = row['artist_id']
        genius_artist_name = row['artist_name']
        spotify_url = row['url']
        print(spotify_url, genius_song_id)


        # SPOTIFY SECTION ------------------------ START ------------------------------------------
        urn = spotify_url.split('/')[-1:][0]
        track = sp.track(urn)
        # TRACK_INFO
        artist_name,artist_uri, track_name ,album_name, track_popularity,explicit,tid,i = show_track(track)
        lyrics = get_lyrics(genius_song_id)
        
        print(lyrics)
        #time.sleep(5)
        print(Back.GREEN +"======>"+ artist_name + " " + track_name)
        print(Style.RESET_ALL)

        #ARTIST_INFO
        artist = sp.artist(artist_uri)
        #pprint.pprint(artist)
        artist_followers = artist['followers']['total']
        artist_genres =",".join(artist['genres'])
        artist_popularity = artist['popularity']

        # AUDIO FEATURES
        audio_features = sp.audio_features(tid)[0]
        #pprint.pprint(audio_features)
        acousticness = audio_features['acousticness']
        danceability = audio_features['danceability']
        duration_ms = audio_features['duration_ms']
        energy = audio_features['energy']
        instrumentalness = audio_features['instrumentalness']
        key = audio_features['key']
        liveness = audio_features['liveness']
        loudness = audio_features['loudness']
        mode = audio_features['mode']
        speechiness = audio_features['speechiness']
        tempo = audio_features['tempo']
        time_signature = audio_features['time_signature']
        valence = audio_features['valence']
        # SPOTIFY SECTION ------------------------ END ------------------------------------------

        #gaurdarndo en dataframe pandas
        db = db.append({'artist':artist_name, 'artist_followers': artist_followers,'artist_genres':artist_genres,
                                    'artist_popularity':artist_popularity,'track_name':track_name,'album_name':album_name,
                                    'track_popularity':track_popularity,'explicit':explicit,'acousticness':acousticness,
                                    'danceability':danceability,'duration_ms':duration_ms,'energy':energy,'instrumentalness':instrumentalness,
                                    'key':key,'liveness':liveness,'loudness':loudness,'mode':mode,'speechiness':speechiness,'tempo':tempo,
                                    'time_signature':time_signature,'valence':valence,'lyrics':lyrics
                                    }, ignore_index=True)


    except:
        pass
#df_artists['artist_id'] = df_artists['artist_id'].astype(int)
db.to_csv('data/db.csv')
