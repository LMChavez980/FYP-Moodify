from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views, status
from ml.data import song_data, lyrics


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

        return_data = {
            "error": "0",
            "message": "Successful",
            "data": [request.data, pl_tracks]
        }

        return Response(return_data)

