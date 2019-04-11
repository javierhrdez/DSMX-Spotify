import requests
import csv
import pandas as pd
import datetime
import time

df_songs = pd.DataFrame() 

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

start_date = datetime.date(2017, 1, 1)
#start_date = datetime.date(2019, 3, 1) 
end_date = datetime.date(2019, 3, 6)

for single_date in daterange(start_date, end_date):
    try:
        fecha = single_date.strftime("%Y-%m-%d")
        print("*"*80)
        print(fecha)
        r = requests.get("https://spotifycharts.com/regional/mx/daily/" + fecha +"/download")
        decoded_content = r.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        my_list = my_list[2:]
        for row in my_list:
            print(row)
            position = row[0]
            track_name = row[1]
            artist = row[2]
            streams = row[3]
            url = row[4]
            df_songs = df_songs.append({'position':position, 'track_name': track_name,'artist':artist,'date':single_date,
                                    'streams':streams,'url':url}, ignore_index=True)
        time.sleep(5)
    except:
        continue




df_songs.to_csv('top_200_spotify.csv')
