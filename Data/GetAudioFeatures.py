import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

CLIENT_ID = "51891ef3095849e98336d9d0c83c05e9"
CLIENT_SECRET = "d833852dd80b4117b0e020e480f142c6"

client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

dataset = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-AudioFeatures.csv", "r", encoding='utf-8')
datareader = csv.reader(dataset)
newfile = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-1866-AudioFeatures.csv", "a+", newline='', encoding='utf-8')
datawriter = csv.writer(newfile)


i = 0
for row in datareader:
    if i == 0:
        i += 1
        datawriter.writerow(row)
        continue
    ret = sp.audio_features(row[6])
    row[7] = ret[0]['danceability']
    row[8] = ret[0]['energy']
    row[9] = ret[0]['key']
    row[10] = ret[0]['loudness']
    row[11] = ret[0]['mode']
    row[12] = ret[0]['speechiness']
    row[13] = ret[0]['acousticness']
    row[14] = ret[0]['instrumentalness']
    row[15] = ret[0]['liveness']
    row[16] = ret[0]['valence']
    row[17] = ret[0]['tempo']
    datawriter.writerow(row)
    print(row)


dataset.close()
newfile.close()
