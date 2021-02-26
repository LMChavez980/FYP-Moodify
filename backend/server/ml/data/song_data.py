import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

bins = {'danceability': ['<= minimum', pd.Interval(0.0768, 0.384), pd.Interval(0.384, 0.506),
                         pd.Interval(0.506, 0.628), pd.Interval(0.628, 0.962), '> maximum'],
        'energy': ['<= minimum', pd.Interval(0.00302, 0.447), pd.Interval(0.447, 0.696),
                   pd.Interval(0.696, 0.879), pd.Interval(0.879, 0.999), '> maximum'],
        'loudness': ['<= minimum', pd.Interval(-34.317, -10.824), pd.Interval(-10.824, -7.541),
                     pd.Interval(-7.541, -5.296), pd.Interval(-5.296, -0.938), '> maximum'],
        'valence': ['<= minimum', pd.Interval(0.0314, 0.226), pd.Interval(0.226, 0.426),
                    pd.Interval(0.426, 0.664), pd.Interval(0.664, 0.982), '> maximum'],
        'tempo': ['<= minimum', pd.Interval(36.958000000000006, 99.387), pd.Interval(99.387, 119.737),
                  pd.Interval(119.737, 140.05), pd.Interval(140.05, 217.396), '> maximum']}

CLIENT_ID = "51891ef3095849e98336d9d0c83c05e9"
CLIENT_SECRET = "d833852dd80b4117b0e020e480f142c6"

client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)


class Track:
    def __init__(self, track_name="NA", track_artists="NA", track_id="NA"):
        self.name = track_name
        self.artists = track_artists,
        self.id = track_id

    def get_trackname(self):
        return self.name

    def get_trackartists(self):
        return self.artists

    def get_trackid(self):
        return self.id

    def set_trackname(self, track_name):
        self.name = track_name

    def set_trackartists(self, track_artists):
        self.artists = track_artists

    def set_trackid(self, track_id):
        self.id = track_id


def get_tracks(playlist_ids):
    sp_pl_ids = dict.fromkeys(playlist_ids, None)

    for pl_id in sp_pl_ids:
        results = sp.playlist_items(playlist_id=pl_id, additional_types=['track'])
        sp_pl_ids[pl_id] = []
        tracks = results['items']
        sp_pl_ids[pl_id].extend(tracks)
        while results['next']:
            results = sp.next(results)
            sp_pl_ids[pl_id].extend(tracks)






    return sp_pl_ids
sp_playlists = ["58gtWgHQ99PHtAkCK2dpYt", "3cejj3mmTgiLrvNCr5qz83", "4yMwcuj91F6OJBvK86hMHu"]
spotify_pl_tks = get_tracks(sp_playlists)
print(spotify_pl_tks)



