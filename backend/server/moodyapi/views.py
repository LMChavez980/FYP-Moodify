from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views
from ml.data import spotify, lyrics
from ml.classifiers import lyrics_sentiment, music_mood
import pandas as pd
from spotipy.exceptions import SpotifyException
from requests.exceptions import HTTPError, Timeout
from moodyapi.models import User, ClassifiedSong
import helpers.dbhelper as dbhelper


# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error": "0",
        "message": "Successful",
    }
    return Response(return_data)


class AnalyzeView(views.APIView):
    def post(self, request):
        try:
            # Get playlist ids and user id
            # saved_tracks = request.get('saved_tracks')
            pl_ids = request.data.get('playlist_ids')
            user_id = request.data.get('user_id')

            # Check if user has used the app before
            dbhelper.check_user_new(user_id=user_id)

            current_user = User.objects.get(user_id=user_id)
            user_tracks = current_user.user_songs

            """# Get tracks of playlist
            pl_tracks = spotify.get_tracks(pl_ids)

            # Get audio features
            pl_tracks = spotify.get_audio_data(pl_tracks)

            # Get lyrics
            pl_tracks = lyrics.get_lyrics(pl_tracks)"""

            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
            #                                    "dummy_song_id_4"], "lyrics": ["", "", "", ""]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3"],
            #                         "lyrics": ["Hello", "Hello", "Hello"]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_5", "dummy_song_id_6", "dummy_song_id_7",
            #                                "dummy_song_id_8"], "lyrics": ["hi", "hi", "hi", "hi"]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
            #                                    "dummy_song_id_5"], "lyrics": ["hi", "hi", "hi", "hi"]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4"],
            #                             "lyrics": ["hi", "hi", "hi"]})
            pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4", "dummy_song_id_5"],
                                         "lyrics": ["hi", "hi", "hi", "hi"], "music mood": ["happy", "sad", "angry", "relaxed"],
                                         "name": ["dummy_song_1", "dummy_song_2", "dummy_song_4", "dummy_song_5"],
                                         "artists": ["dummy_artist", "dummy_artist_2", "dummy_artist_4", "dummy_artist_5"]})

            # Lyrics to Dataframe
            # pl_tracks_df = pd.DataFrame.from_dict(pl_tracks)

            # new_tracks_df = pl_tracks_df[pl_tracks_df.lyrics != ""]

            # Remove any rows where song lyrics were not found
            # Check for any songs that have been analysed before
            #   - if yes skip ML process and get songs that have been analysed that are part of tracks
            #   - If no then go to ML process and add new songs to ClassifiedSongs table
            #   - Any existing or new songs add to user songs
            is_empty, new_tracks_df, existing_tracks = dbhelper.check_empty(pl_tracks_df, user_tracks)

            if (not is_empty) and (new_tracks_df is not None):
                """ # Initialize the sentiment analyzer
                senti_analysis = lyrics_sentiment.LyricsSentiment()

                # Preprocess the lyrics - expand contractions, remove punctuations etc.
                new_tracks_df["lyrics"].apply(senti_analysis.preprocess)

                # Get sentiment for the lyrics
                new_tracks_df["lyrics sentiment"] = senti_analysis.sentiment(new_tracks_df["lyrics"])

                musicmood = music_mood.MusicMood()

                # Bin the continuous values
                for col in music_mood.bins.keys():
                    new_tracks_df[col + " binned"] = musicmood.preprocess(col, new_tracks_df[col])

                # Get music mood
                test_features = ["lyrics sentiment", "mode", "danceability binned", "energy binned", "loudness binned",
                                 "valence binned", "tempo binned"]

                new_tracks_df["music mood"] = musicmood.mood(new_tracks_df[test_features])"""

                new_track_ids = list(new_tracks_df["id"].values)
                new_track_names = list(new_tracks_df["name"].values)
                new_track_artists = list(new_tracks_df["artists"].values)
                new_track_moods = list(new_tracks_df["music mood"].values)

                # Create bulk insert for new classified songs
                new_tracks_inserts = []
                for i in range(len(new_track_ids)):
                    new_tracks_inserts.append(ClassifiedSong(song_id=new_track_ids[i], song_name=new_track_names[i],
                                                             artists=new_track_artists[i], mood=new_track_moods[i]))

                ClassifiedSong.objects.bulk_create(new_tracks_inserts, ignore_conflicts=True)

               #print(new_tracks_df[["name", "artists", "lyrics sentiment", "music mood"]])
                print(new_tracks_df[["name", "artists", "music mood"]])

                if existing_tracks is not None:
                    # Add the existing analysed songs to user_songs and new songs
                    existing = list(existing_tracks["id"].values)
                    existing.extend(new_track_ids)
                    print(existing)
                    current_user.user_songs.extend(existing)
                    current_user.save()
                    return_data = {
                        "error": "0",
                        "message": "Added songs to database and user pool",
                        "data": [request.data, new_tracks_df["id"], existing_tracks["id"]],
                    }
                else:
                    # Add the newly analysed songs to user_songs
                    current_user.user_songs.extend(new_track_ids)
                    current_user.save()
                    return_data = {
                        "error": "0",
                        "message": "Added songs to database and user pool",
                        "data": [request.data, new_tracks_df["id"]],
                    }
            # If songs don't need reclassification or adding to user
            elif (not is_empty) and (new_tracks_df is None) and (existing_tracks is None):
                return_data = {
                    "error": "0",
                    "message": "No new additions made to song pool"
                }
            # If songs don't need to be classified but need to be added to user
            elif (not is_empty) and (new_tracks_df is None) and (existing_tracks is not None):
                # current_user_obj = User.objects.get(user_id=user_id)
                # current_user_obj.user_songs.extend(existing_tracks["id"])
                # current_user_obj.save()
                return_data = {
                    "error": "0",
                    "message": "{} songs added to song pool"
                }
            # if no songs returned due to no lyrics
            else:
                return_data = {
                    "error": "4",
                    "message": "Moodify currently does not support songs without lyrics - The songs analysed did not "
                               "contain lyrics or lyrics could not be sourced"
                }

        except (HTTPError, Timeout, SpotifyException, TypeError) as e:
            if type(e) == HTTPError:
                return_data = {
                    "error": "1",
                    "message": "There was a HTTP Error in the Moodify process - Please try again",
                }
            elif type(e) == Timeout:
                return_data = {
                    "error": "2",
                    "message": "There was a Timeout Error in the Moodify process - Please try again"
                }
            elif type(e) == SpotifyException:
                return_data = {
                    "error": "3",
                    "message": "There was a Spotify Error in the Moodify process - Please try again"
                }
            elif type(e) == TypeError:
                print(e)
                return_data = {
                    "error": "5",
                    "message": "There was an error in the Moodify process - Please try again"
                }

        return Response(return_data)
