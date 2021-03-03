import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius as lg


CLIENT_ID = "51891ef3095849e98336d9d0c83c05e9"
CLIENT_SECRET = "d833852dd80b4117b0e020e480f142c6"

client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

result = sp.playlist_items(playlist_id="58gtWgHQ99PHtAkCK2dpYt", additional_types=['track'], market='IE')
tracks = result['items']

while result['next']:
    result = sp.next(result)
    tracks.extend(result['items'])

print(tracks)

tracks_dict = dict.fromkeys(["title", "artist"], "")

titles = []
artists = []

for item in tracks:
    titles.append(item['track']['name'])
    artists.append(item['track']['artists'][0]['name'])

tracks_dict["title"] = titles
tracks_dict["artist"] = artists

print(tracks_dict["title"])
print(tracks_dict["artist"])

GENIUS_CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'
genius = lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)
genius.remove_section_headers = True
genius.retries = 3
genius.timeout = 10

for i in range(len(tracks_dict["title"])):
    song = genius.search_song(title=tracks_dict["title"][i], artist=tracks_dict["artist"][i])
    print("Title:", song.title)
    print("Artist:", song.artist, "\n")

