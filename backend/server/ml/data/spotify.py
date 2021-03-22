import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from requests.exceptions import HTTPError, Timeout
from spotipy.exceptions import SpotifyException

CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d"
CLIENT_SECRET = "d940799ff9554e9fa9cf28ccd54d5850"


def get_tracks(playlist_ids, include_save_tracks, auth_token):
    try:
        client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

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

        # If saved tracks has been included add them to list
        if include_save_tracks:
            user_tracks = get_user_saved(auth_token)
            sp_pl_tracks.extend(user_tracks)

        for item in sp_pl_tracks:
            # Exclude duplicates
            if item['track']['id'] not in id_list:
                t_id = item['track']['id']
                name = item['track']['name']
                artist = item['track']['artists'][0]['name']
                id_list.append(t_id)
                name_list.append(name)
                artist_list.append(artist)

        sp_track_meta["id"] = id_list
        sp_track_meta["name"] = name_list
        sp_track_meta["artists"] = artist_list

        return sp_track_meta

    except (SpotifyException, HTTPError, Timeout) as e:
        print(e)
        raise e


def get_audio_data(sp_tracks):
    try:
        client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

        audio_ft = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                    "instrumentalness",
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
            # speechiness.append(result[0]['speechiness'])
            # acousticness.append(result[0]['acousticness'])
            # instrumentalness.append(result[0]['instrumentalness'])
            # liveness.append(result[0]['liveness'])
            valence.append(result[0]['valence'])
            tempo.append(result[0]['tempo'])

        sp_tracks['danceability'] = danceability
        sp_tracks['energy'] = energy
        sp_tracks['key'] = key
        sp_tracks['loudness'] = loudness
        sp_tracks['mode'] = mode
        # sp_tracks['speechiness'] = speechiness
        # sp_tracks['acousticness'] = acousticness
        # sp_tracks['instrumentalness'] = instrumentalness
        # sp_tracks['liveness'] = liveness
        sp_tracks['valence'] = valence
        sp_tracks['tempo'] = tempo

        return sp_tracks
    except (SpotifyException, HTTPError, Timeout) as e:
        print(e)
        raise e


def get_user_saved(auth_token):
    try:
        user_saved_tracks = []
        sp = spotipy.Spotify(auth=auth_token)

        results = sp.current_user_saved_tracks(limit=50)
        user_saved_tracks.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            tracks = results['items']
            user_saved_tracks.extend(tracks)

        return user_saved_tracks
    except (SpotifyException, HTTPError, Timeout) as e:
        print(e)
        raise e


def create_playlist(userid, mood, tracks, pl_index, auth_token):
    playlist_name = "Moodify {mood} Playlist {index}".format(mood=mood, index=pl_index)
    playlist_id = ""
    user_playlists = []
    playlist_desc = "Playlist created using moodify"

    try:
        sp = spotipy.Spotify(auth_token)

        sp.user_playlist_create(user=userid, name=playlist_name, description=playlist_desc)

        result = sp.user_playlists(userid)

        user_playlists.extend(result['items'])

        while result['next']:
            result = sp.next(result)
            user_playlists.extend(result['items'])

        for pl in user_playlists:
            if pl["name"] == playlist_name:
                playlist_id = pl["id"]

        if playlist_id != "":
            sp.playlist_add_items(playlist_id=playlist_id, items=tracks)
            return playlist_id
        else:
            return None

    except (SpotifyException, HTTPError, Timeout) as e:
        print(e)
        raise e

# sp_playlists = ["58gtWgHQ99PHtAkCK2dpYt", "3cejj3mmTgiLrvNCr5qz83", "4yMwcuj91F6OJBvK86hMHu"]
# sp_playlists = ["58gtWgHQ99PHtAkCK2dpYt"]
# spotify_pl_tks = get_tracks(sp_playlists)
# spotify_pl_tks = get_audio_data(spotify_pl_tks)
# print(spotify_pl_tks["id"])
#pl_id = create_playlist(userid="lmchavez980", mood="Happy", tracks=["dummy_song"], pl_index=0, auth_token=auth)
#print(pl_id)
# for key in spotify_pl_tks.keys():
#    print(spotify_pl_tks[key], "\n", len(spotify_pl_tks[key]))
