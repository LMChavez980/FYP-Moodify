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


def get_tracks(playlist_ids):
    sp_pl_tracks = []

    for pl_id in playlist_ids:
        results = sp.playlist_items(playlist_id=pl_id, additional_types=['track'])
        tracks = results['items']
        sp_pl_tracks.extend(tracks)
        while results['next']:
            results = sp.next(results)
            tracks = results['items']
            sp_pl_tracks.extend(tracks)

    sp_track_meta = dict.fromkeys(["id", "name", "artists"], "")
    id_list = []
    name_list = []
    artist_list = []

    for item in sp_pl_tracks:
        id = item['track']['id']
        name = item['track']['name']
        artist = item['track']['artists'][0]['name']
        id_list.append(id)
        name_list.append(name)
        artist_list.append(artist)

    sp_track_meta["id"] = id_list
    sp_track_meta["name"] = name_list
    sp_track_meta["artists"] = artist_list

    return sp_track_meta


def get_audio_data(sp_tracks):
    audio_ft = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness",
                "liveness", "valence", "tempo"]

    for ft in audio_ft:
        sp_tracks[ft] = ""

    danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo = \
        [], [], [], [], [], [], [], [], [], [], []

    for track_id in sp_tracks['id']:
        result = sp.audio_features(track_id)
        danceability.append(result[0]['danceability'])
        energy.append(result[0]['energy'])
        key.append(result[0]['key'])
        loudness.append(result[0]['loudness'])
        mode.append(result[0]['mode'])
        speechiness.append(result[0]['speechiness'])
        acousticness.append(result[0]['acousticness'])
        instrumentalness.append(result[0]['instrumentalness'])
        liveness.append(result[0]['liveness'])
        valence.append(result[0]['valence'])
        tempo.append(result[0]['tempo'])

    sp_tracks['danceability'] = danceability
    sp_tracks['energy'] = energy
    sp_tracks['key'] = key
    sp_tracks['loudness'] = loudness
    sp_tracks['mode'] = mode
    sp_tracks['speechiness'] = speechiness
    sp_tracks['acousticness'] = acousticness
    sp_tracks['instrumentalness'] = instrumentalness
    sp_tracks['liveness'] = liveness
    sp_tracks['valence'] = valence
    sp_tracks['tempo'] = tempo

    return sp_tracks


#sp_playlists = ["58gtWgHQ99PHtAkCK2dpYt", "3cejj3mmTgiLrvNCr5qz83", "4yMwcuj91F6OJBvK86hMHu"]
#sp_playlists = ["58gtWgHQ99PHtAkCK2dpYt"]
spotify_pl_tks = get_tracks(sp_playlists)
spotify_pl_tks = get_audio_data(spotify_pl_tks)

#for key in spotify_pl_tks.keys():
#    print(spotify_pl_tks[key], "\n", len(spotify_pl_tks[key]))
