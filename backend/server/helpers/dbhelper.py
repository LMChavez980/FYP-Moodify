from moodyapi.models import User, ClassifiedSong, MoodPlaylist
import pandas as pd

"""
    This is a class for helper python file for functions related to accessing the database
"""


"""
Function to check if user is already in the database
Parameters: user id
Returns: NA (raises exception if the passed user_id is an empty string)
"""


def check_user_new(user_id):
    # If the user is new add them to the database
    # Else if user exists already, get their tracks
    if user_id.strip() == "":
        raise Exception('NEW001', 'Blank user')

    if not User.objects.filter(user_id=user_id).exists():
        new_user = User(user_id=user_id, user_songs=[])
        new_user.save()


"""
Function to check if the songs to classify already exist in the database
Parameters: DataFrame of tracks to classify, list of user analysed tracks
Returns: boolean status for DataFrame, DataFrame or None for tracks to classify, DataFrame or None for classified tracks
to assign to the user
"""


def check_empty(tracks_df, user_analysed):
    # print(tracks_df)
    # print(user_analysed)

    # Check if there are tracks is empty
    if not tracks_df.empty:
        moodify_tracks = ClassifiedSong.objects.all().values_list('song_id', flat=True)

        # Get previously analysed tracks in database
        analysed_tracks = tracks_df[tracks_df.id.isin(moodify_tracks)]

        # print("Analysed:", analysed_tracks['id'])

        # If no analysed songs in the database or if all the tracks are new
        # Go through classification for all tracks
        if moodify_tracks.count() == 0 or analysed_tracks.empty:
            print("All new tracks")
            return False, tracks_df, None
        else:
            # Get tracks not in database
            new_tracks = tracks_df[~tracks_df.id.isin(moodify_tracks)]

            # print("moodify new tracks:", new_tracks['id'])

            # Get tracks that have been analysed but not been assigned to user
            user_new_tracks = analysed_tracks[~analysed_tracks.id.isin(user_analysed)]

            # print("user new tracks:", user_new_tracks['id'])

            # if all the tracks to classify have been analysed before but have not been assigned to the user
            # if some of the tracks to classify have been analysed before have been assigned to the user
            # but there are new tracks to classify
            # if there are new tracks that haven't been classified as well as track that have been classified
            # but not assigned to the user
            # If all the tracks to classify have been classified and have been assigned to user
            if not user_new_tracks.empty and new_tracks.empty:
                print("Test 5 Exit: All analysed but not assigned to user")
                return False, None, user_new_tracks
            elif user_new_tracks.empty and not new_tracks.empty:
                print("Test 4 Exit: New tracks to add to database but all analysed have been assigned to user")
                return False, new_tracks, None
            elif not user_new_tracks.empty and not new_tracks.empty:
                print("Test 6 Exit: New tracks and existing tracks to add to user pool")
                return False, new_tracks, user_new_tracks
            else:
                print("Test 2 Exit: No new tracks to assign")
                return False, None, None

    return True, None, None


"""
test_df1 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
                                "dummy_song_id_4"], "lyrics": ["", "", "", ""]})
test_df2 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3"],
                         "lyrics": ["Hello", "Hello", "Hello"]})
test_df3 = pd.DataFrame({"id": ["dummy_song_id_5", "dummy_song_id_6", "dummy_song_id_7",
                                "dummy_song_id_8"], "lyrics": ["hi", "hi", "hi", "hi"]})
test_df4 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
                                "dummy_song_id_5"], "lyrics": ["hi", "hi", "hi", "hi"]})
test_df5 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4"],
                         "lyrics": ["hi", "hi", "hi"]})
user_songs = User.objects.filter(user_id='dummy_user').values_list('user_songs', flat=True)


# no lyrics
empty, ret_df, ret_user_tracks = check_empty(test_df1, user_songs[0])
print("Test 1 Result:", empty, ret_df, ret_user_tracks)
# all songs user has assigned and in database
empty, ret_df, ret_user_tracks = check_empty(test_df2, user_songs[0])
print("Test 2 Result:", empty, ret_df, ret_user_tracks)
# all new songs
empty, ret_df, ret_user_tracks = check_empty(test_df3, user_songs[0])
print("Test 3 Result:", empty, ret_df, ret_user_tracks)
# 1 new song and others already existing user songs
empty, ret_df, ret_user_tracks = check_empty(test_df4, user_songs[0])
print("Test 4 Result:", empty, ret_df, ret_user_tracks)
# All existing songs but 1 track not with user
empty, ret_df, ret_user_tracks = check_empty(test_df5, user_songs[0])
print("Test 5 Result:", empty, ret_df, ret_user_tracks)
"""
