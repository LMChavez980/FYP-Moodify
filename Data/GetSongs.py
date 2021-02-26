import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "51891ef3095849e98336d9d0c83c05e9"
CLIENT_SECRET = "d833852dd80b4117b0e020e480f142c6"

client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

result = sp.playlist_items(playlist_id="4b1Ea2rqiJl57ZKC2IPymd", additional_types=['track'], market='IE')
tracks = result['items']
print("Start", len(tracks))
while result['next']:
    print(result['next'])
    result = sp.next(result)
    tracks.extend(result['items'])
    print("New:", len(tracks))

print(len(tracks))



