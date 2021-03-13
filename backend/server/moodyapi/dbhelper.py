from moodyapi.models import User, ClassifiedSong, MoodPlaylist

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
        moodify_tracks = ClassifiedSong.objects.all()

        # Only if application is new
        # If no analysed songs in system db add them - assume user has none too
        if moodify_tracks.count() != 0:
            tracks_df = tracks_df[~tracks_df.id.isin(moodify_tracks)]

            # Check for matches in user's analysed songs
            # If
            if not tracks_df.empty():
                if len(user_analysed) != 0:
                    tracks_df = tracks_df[~tracks_df.id.isin(user_analysed)]

                    if not tracks_df.empty():
                        return False, tracks_df
                else:
                    return False, tracks_df
        else:
            return False, tracks_df

    return True, tracks_df, 1
