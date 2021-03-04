from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views, status
from ml.data import song_data, lyrics
from ml.classifiers import lyrics_sentiment, music_mood
import pandas as pd


# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)


class AnalyzeView(views.APIView):
    def post(self, request):
        # Get playlist ids
        pl_ids = request.data.get('playlist_ids')

        # Get tracks of playlist
        pl_tracks = song_data.get_tracks(pl_ids)

        # Get audio features
        pl_tracks = song_data.get_audio_data(pl_tracks)

        # Get lyrics
        pl_tracks = lyrics.get_lyrics(pl_tracks)

        # Lyrics to Dataframe
        pl_tracks_df = pd.DataFrame.from_dict(pl_tracks)

        # Remove any rows where song lyrics were not found
        pl_tracks_df = pl_tracks_df[pl_tracks_df.lyrics != ""]

        # Initialize the sentiment analyzer
        senti_analysis = lyrics_sentiment.LyricsSentiment()

        # Preprocess the lyrics - expand contractions, remove punctuations etc.
        pl_tracks_df["lyrics"].apply(senti_analysis.preprocess)

        # Get sentiment for the lyrics
        pl_tracks_df["lyrics sentiment"] = senti_analysis.sentiment(pl_tracks_df["lyrics"])

        print(pl_tracks_df[["name", "artists", "lyrics sentiment"]])

        musicmood = music_mood.MusicMood()

        # Bin the continuous values
        for col in music_mood.bins.keys():
            pl_tracks_df[col + " binned"] = musicmood.preprocess(col, pl_tracks_df[col])

        # Get music mood
        test_features = ["lyrics sentiment", "mode", "danceability binned", "energy binned", "loudness binned", "valence binned",
                         "tempo binned"]
        pl_tracks_df["music mood"] = musicmood.mood(pl_tracks_df[test_features])

        print(pl_tracks_df[["name", "artists", "lyrics sentiment", "music mood"]])

        return_data = {
            "error": "0",
            "message": "Successful",
            "data": [request.data, pl_tracks]
        }

        return Response(return_data)