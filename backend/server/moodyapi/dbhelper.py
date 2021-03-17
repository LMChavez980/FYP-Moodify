from moodyapi.models import User, ClassifiedSong, MoodPlaylist
import pandas as pd

"""
    This is a class for helper python file for functions related to accessing the database
"""


def check_user_new(user_id):
    # If the user is new add them to the database
    # Else if user exists already, get their tracks
    if not User.objects.filter(user_id=user_id).exists():
        new_user = User(user_id=user_id, user_songs=[])
        new_user.save()


def check_empty(tracks_df, user_analysed):
    # Remove songs with no lyrics
    tracks_df = tracks_df[tracks_df.lyrics != ""]

    # Check if there are tracks remaining
    if not tracks_df.empty():
        moodify_tracks = ClassifiedSong.objects.all().values_list('song_id', flat=True)

        # Get previously analysed tracks in database
        analysed_tracks = tracks_df[tracks_df.id.isin(moodify_tracks)]

        # If no analysed songs in the database or if all the tracks are new - assumes user has none too
        # Go through classification for all tracks
        if moodify_tracks.count() == 0 or analysed_tracks.empty:
            user_new_tracks = tracks_df["id"]
            return False, tracks_df, user_new_tracks
        elif analysed_tracks.count() == moodify_tracks.count():  # If all of the tracks are already analysed
            # Get tracks that user has out of analysed tracks
            user_new_tracks = analysed_tracks[~analysed_tracks.id.isin(user_analysed)]

            if user_new_tracks.count() != 0:
                return False, None, user_new_tracks
            else:
                return False, None, None

        else:
            # Get tracks not in database
            new_tracks = tracks_df[~tracks_df.id.isin(moodify_tracks)]

            # Get tracks that user has out of analysed tracks
            user_new_tracks = analysed_tracks[~analysed_tracks.id.isin(user_analysed)]

            return False, new_tracks, user_new_tracks

    return True, None, None

test_df = pd.DataFrame()
empty, ret1, ret2 = check_empty()