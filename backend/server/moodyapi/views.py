from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views
from ml.data import spotify, lyrics
from ml.classifiers import lyrics_sentiment, music_mood
import pandas as pd
from spotipy.exceptions import SpotifyException
from requests.exceptions import HTTPError, Timeout
from moodyapi.models import User, ClassifiedSong, MoodPlaylist
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
            saved_tracks = request.data.get('saved_tracks')
            token = request.data.get('auth_token')
            pl_ids = request.data.get('playlist_ids')
            user_id = request.data.get('user_id')

            print(request.data)

            if saved_tracks == "1":
                saved_tracks = True
            else:
                saved_tracks = False

            # Check if user has used the app before
            dbhelper.check_user_new(user_id=user_id)

            current_user = User.objects.get(user_id=user_id)
            user_tracks = current_user.user_songs

            # Get tracks of playlist
            pl_tracks = spotify.get_tracks(pl_ids, saved_tracks, token)

            # Get audio features
            pl_tracks = spotify.get_audio_data(pl_tracks)

            # Get lyrics
            pl_tracks = lyrics.get_lyrics(pl_tracks)

            pl_tracks_df = pd.DataFrame.from_dict(pl_tracks)

            # pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
            #                                    "dummy_song_id_4"], "lyrics": ["", "", "", ""]})
            # pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3"],
            #                         "lyrics": ["Hello", "Hello", "Hello"]})
            # pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_5", "dummy_song_id_6", "dummy_song_id_7",
            #                                "dummy_song_id_8"], "lyrics": ["hi", "hi", "hi", "hi"]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
            #                                    "dummy_song_id_5"], "lyrics": ["hi", "hi", "hi", "hi"]})
            # pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4"],
            #                             "lyrics": ["hi", "hi", "hi"]})
            #pl_tracks_df = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4", "dummy_song_id_5"],
            #                             "lyrics": ["hi", "hi", "hi", "hi"], "music mood": ["happy", "sad", "angry", "relaxed"],
            #                             "name": ["dummy_song_1", "dummy_song_2", "dummy_song_4", "dummy_song_5"],
            #                             "artists": ["dummy_artist", "dummy_artist_2", "dummy_artist_4", "dummy_artist_5"]})


            # Remove any rows where song lyrics were not found
            # Check for any songs that have been analysed before
            #   - if yes skip ML process and get songs that have been analysed that are part of tracks
            #   - If no then go to ML process and add new songs to ClassifiedSongs table
            #   - Any existing or new songs add to user songs
            is_empty, new_tracks_df, existing_tracks = dbhelper.check_empty(pl_tracks_df, user_tracks)

            if (not is_empty) and (new_tracks_df is not None):
                # Initialize the sentiment analyzer
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

                new_tracks_df["music mood"] = musicmood.mood(new_tracks_df[test_features])

                new_track_ids = list(new_tracks_df["id"].values)
                new_track_names = list(new_tracks_df["name"].values)
                new_track_artists = list(new_tracks_df["artists"].values)
                new_track_moods = list(new_tracks_df["music mood"].values)

                # Create bulk insert for new classified songs
                #new_tracks_inserts = []
                #for i in range(len(new_track_ids)):
                #    new_tracks_inserts.append(ClassifiedSong(song_id=new_track_ids[i], song_name=new_track_names[i],
                #                                           artists=new_track_artists[i], mood=new_track_moods[i]))

                #ClassifiedSong.objects.bulk_create(new_tracks_inserts, ignore_conflicts=True)

                print(new_tracks_df[["name", "artists", "lyrics sentiment", "music mood"]])
                # print(new_tracks_df[["name", "artists", "music mood"]])

                if existing_tracks is not None:
                    print("Existing:\n", existing_tracks)
                    #Add the existing analysed songs to user_songs and new songs
                    #existing = list(existing_tracks["id"].values)
                    #existing.extend(new_track_ids)
                    #print(existing)
                    #current_user.user_songs.extend(existing)
                    #current_user.save()
                    return_data = {
                        "error": "0",
                        "message": "Added songs to database and user pool"
                        #"data": [new_tracks_df['id'], existing_tracks['id']]
                    }
                else:
                    # Add the newly analysed songs to user_songs
                    #current_user.user_songs.extend(new_track_ids)
                    #current_user.save()
                    return_data = {
                        "error": "0",
                        "message": "Added songs to database and user pool"
                        #"data": [new_tracks_df['id']]
                    }
            # If songs don't need reclassification or adding to user
            elif (not is_empty) and (new_tracks_df is None) and (existing_tracks is None):
                return_data = {
                    "error": "0",
                    "message": "No new additions made to song pool"
                }
            # If songs don't need to be classified but need to be added to user
            elif (not is_empty) and (new_tracks_df is None) and (existing_tracks is not None):
                #current_user_obj = User.objects.get(user_id=user_id)
                #current_user_obj.user_songs.extend(existing_tracks["id"])
                #current_user_obj.save()
                return_data = {
                    "error": "0",
                    "message": "{} songs added to song pool",
                    "data": [existing_tracks['id']]
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


class GeneratePlaylist(views.APIView):
    def post(self, request):
        try:

            # user_id, auth_token, mood_selected
            userid = request.data.get('user_id')
            auth = request.data.get('auth_token')
            user_mood = request.data.get('mood_selected')

            print(userid, "\n", auth, "\n", user_mood)

            # Check if user exists
            dbhelper.check_user_new(user_id=userid)

            # Check if user has songs in db and in the mood category selected
            user_tracks = User.objects.values_list('user_songs', flat=True).filter(user_id=userid)[0]

            if len(user_tracks) != 0:
                mood_tracks = ClassifiedSong.objects.values_list('song_id', flat=True).filter(song_id__in=user_tracks, mood=user_mood)

                if len(mood_tracks) != 0:
                    # Get mood playlist index - add one in case it's 0
                    playlist_track_no = MoodPlaylist.objects.filter(user_id=userid, mood=user_mood).count() + 1

                    # If there is proceed to create the playlist
                    new_playlist_id = spotify.create_playlist(userid, user_mood, mood_tracks, playlist_track_no, auth)

                    if new_playlist_id is not None:
                        MoodPlaylist.objects.create(playlist_id=new_playlist_id, user_id_id=userid, mood=user_mood)

                        return_data = {
                            "error": "0",
                            "message": "Playlist Created Successfully",
                            "data": {"new_playlist_id": new_playlist_id}
                        }
                    else:
                        return_data = {
                            "error": "5",
                            "message": "Playlist could not be created. There was an error in the Moodify process - Please "
                                       "try again "
                        }
                else:
                    return_data = {
                        "error": "5",
                        "message": "Playlist could not be created. You do not have any analysed tracks"
                    }
            else:
                return_data = {
                    "error": "5",
                    "message": "Playlist could not be created. You do not have any analysed tracks"
                }
        except Exception as e:
            print(e.args)
            return_data = {
                "error": "1",
                "message": "An error has occured"
            }

        return Response(return_data)


@api_view(['POST'])
def mood_statistics(request):
    try:
        user_id = request.data.get('user_id')

        # Check if user has used the app before
        dbhelper.check_user_new(user_id=user_id)

        # Get user songs
        user_tracks = User.objects.values_list('user_songs', flat=True).filter(user_id=user_id)[0]

        if len(user_tracks) != 0:
            moods = ["happy", "sad", "angry", "relaxed"]
            mood_count = dict.fromkeys(moods, 0)

            for emo in moods:
                mood_count[emo] = ClassifiedSong.objects.filter(song_id__in=user_tracks, mood=emo).count()

            return_data = {
                "error": "0",
                "message": "Statistics retrieved",
                "data": mood_count
            }
        else:
            return_data = {
                "error": "0",
                "message": "No songs in your pool - Add to pool"
            }
    except Exception as e:
        print(e.args)
        return_data = {
            "error": "0",
            "message": "An Error Occured: Could not load statistics"
        }

    return Response(return_data)
