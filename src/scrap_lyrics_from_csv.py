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
SPOTIFY_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
SPOTIFY_CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
JAVIER_ID = 'XXXXXXXXXXXXXXXXXXXXXXXX'


#GENIUS API (EXTRACCION DE LETRAS)
GENIUS_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)





#print(Fore.RED + 'some red text')
#print(Back.GREEN + 'and with a green background')
#print(Style.DIM + 'and in dim text')
#print(Style.RESET_ALL)


df_songs = pd.DataFrame()

def get_jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c)), str1



def get_lyrics(q):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    search_url = base_url + '/search'
    data = {'q': q}
    coef_max = 0.0
    try:
        response = requests.get(search_url, data=data, headers=headers)
        response = json.loads(response.content)
        pprint.pprint(response)
        hits = response.get('response').get('hits')
        coeficientes = []
        canciones = []
        for hit in hits:
            #print(hit)
            titulo = hit.get('result').get('full_title')
            coeficientes.append(get_jaccard_sim(titulo, q))
            canciones.append(titulo)
            print(get_jaccard_sim(titulo, q))
        coef_max, cancion = max(coeficientes)
        print("MAX:",coef_max)
        print("CANCION:",cancion)
        if coef_max == 0.0 :
            raise Exception("No coincide ninguna cancion :(") 
        indice_elegida = canciones.index(cancion)
        #print("ELEGIDA", indice_elegida)

        # EXTRAE CANCION DESDE GENIUS
        response = requests.get(base_url + hits[indice_elegida].get('result').get('api_path'), headers=headers)
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
        return coef_max,lyrics
    except:
        return coef_max,""


#spotify:user:spotifycharts:playlist:37i9dQZEVXbO3qyFxbkOE1 Mexico Top 50

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        #print(track)
        #print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
        #print(i,track['artists'][0]['name'], track['name'])
        artists = [artist['name'] for artist in track['artists']]
        #print("\n")
        #print("artistas:", ",".join(artists))
        album = track['album']
        album_name = album['name']
        #print("album:", album)
        #considerando solo el primer artista de la cancion
        #yield track['artists'][0]['name'],track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i
        #considerando todos los artistas de la cancion
        yield ",".join(artists),track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i

def show_track(track):

    artists = [artist['name'] for artist in track['artists']]
    album = track['album']
    album_name = album['name']
    #considerando solo el primer artista de la cancion
    #yield track['artists'][0]['name'],track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i
    #considerando todos los artistas de la cancion
    return ",".join(artists),track['artists'][0]['uri'], track['name'],album_name,track['popularity'],track['explicit'],track['uri'], i



music = pd.read_csv("top_200_unicos.csv")
for i,row in music.iterrows():
    artist = row['artist']
    track_name = row['track_name']
    url = row['url']
    #print(artist, track_name , url)
    urn = url.split('/')[-1:][0]
    track = sp.track(urn)
    #pprint.pprint(track)
    # TRACK_INFO
    artist_name,artist_uri, track_name ,album_name, track_popularity,explicit,tid,i = show_track(track)
    jaccard,lyrics = get_lyrics(artist_name.split(',')[0] + " " + track_name)
    #time.sleep(5)
    print(Back.GREEN +"======>"+ artist_name + " " + track_name)
    print(Style.RESET_ALL)
    #print("======>",cantante,"-", titulo)

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

    #gaurdarndo en dataframe pandas
    df_songs = df_songs.append({'jaccard':jaccard,'artist':artist_name, 'artist_followers': artist_followers,'artist_genres':artist_genres,
                                 'artist_popularity':artist_popularity,'track_name':track_name,'album_name':album_name,
                                 'track_popularity':track_popularity,'explicit':explicit,'acousticness':acousticness,
                                'danceability':danceability,'duration_ms':duration_ms,'energy':energy,'instrumentalness':instrumentalness,
                                'key':key,'liveness':liveness,'loudness':loudness,'mode':mode,'speechiness':speechiness,'tempo':tempo,
                                'time_signature':time_signature,'valence':valence,'lyrics':lyrics
                                }, ignore_index=True)

    print(Fore.RED + lyrics)
    print(Style.RESET_ALL)
    time.sleep(0.5)

df_songs.to_csv('spotify_1976_jaccard.csv')