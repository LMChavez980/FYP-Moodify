from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views, status
from ml.data import spotify, lyrics
from ml.classifiers import lyrics_sentiment, music_mood
import pandas as pd
from spotipy.exceptions import SpotifyException
from requests.exceptions import HTTPError, Timeout


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
            # Get playlist ids
            pl_ids = request.data.get('playlist_ids')

            # Get tracks of playlist
            pl_tracks = spotify.get_tracks(pl_ids)

            # Get audio features
            pl_tracks = spotify.get_audio_data(pl_tracks)

            # Get lyrics
            pl_tracks = lyrics.get_lyrics(pl_tracks)

            # Lyrics to Dataframe
            pl_tracks_df = pd.DataFrame.from_dict(pl_tracks)

            # Remove any rows where song lyrics were not found
            pl_tracks_df = pl_tracks_df[pl_tracks_df.lyrics != ""]

            if not pl_tracks_df.empty:
                # Initialize the sentiment analyzer
                senti_analysis = lyrics_sentiment.LyricsSentiment()

                # Preprocess the lyrics - expand contractions, remove punctuations etc.
                pl_tracks_df["lyrics"].apply(senti_analysis.preprocess)

                # Get sentiment for the lyrics
                pl_tracks_df["lyrics sentiment"] = senti_analysis.sentiment(pl_tracks_df["lyrics"])

                musicmood = music_mood.MusicMood()

                # Bin the continuous values
                for col in music_mood.bins.keys():
                    pl_tracks_df[col + " binned"] = musicmood.preprocess(col, pl_tracks_df[col])

                # Get music mood
                test_features = ["lyrics sentiment", "mode", "danceability binned", "energy binned", "loudness binned",
                                 "valence binned", "tempo binned"]

                pl_tracks_df["music mood"] = musicmood.mood(pl_tracks_df[test_features])

                print(pl_tracks_df[["name", "artists", "lyrics sentiment", "music mood"]])

                return_data = {
                    "error": "0",
                    "message": "Successful",
                    "data": [request.data, pl_tracks]
                }
            else:
                return_data = {
                    "error": "4",
                    "message": "Could not find lyrics for songs selected - Moodify currently does not support songs "
                               "without lyrics"
                }

        except (HTTPError, Timeout, SpotifyException, TypeError) as e:
            if type(e) == HTTPError:
                request_data = {
                    "error": "1",
                    "message": "There was a HTTP Error in the Moodify process - Please try again",

                }
            elif type(e) == Timeout:
                request_data = {
                    "error": "2",
                    "message": "There was a Timeout Error in the Moodify process - Please try again"
                }
            elif type(e) == SpotifyException:
                request_data = {
                    "error": "3",
                    "message": "There was a Spotify Error in the Moodify process - Please try again"
                }
            elif type(e) == TypeError:
                return_data = {
                    "error": "5",
                    "message": "There was an error in the Moodify process - Please try again"
                }

        return Response(return_data)