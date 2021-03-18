from unittest import TestCase
from helpers import dbhelper
import pandas as pd
from moodyapi.models import User


class Test(TestCase):
    def setUp(self):
        # df for no lyrics
        self.test_df1 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
                                             "dummy_song_id_4"], "lyrics": ["", "", "", ""]})
        # df for all songs user has and in database
        self.test_df2 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3"],
                                      "lyrics": ["Hello", "Hello", "Hello"]})
        # df for all new songs
        self.test_df3 = pd.DataFrame({"id": ["dummy_song_id_5", "dummy_song_id_6", "dummy_song_id_7",
                                             "dummy_song_id_8"], "lyrics": ["hi", "hi", "hi", "hi"]})
        # df for 1 new song and other existing user songs
        self.test_df4 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_3",
                                             "dummy_song_id_5"], "lyrics": ["hi", "hi", "hi", "hi"]})
        # df for all existing songs in database but not with user
        self.test_df5 = pd.DataFrame({"id": ["dummy_song_id_1", "dummy_song_id_2", "dummy_song_id_4"],
                                      "lyrics": ["hi", "hi", "hi"]})
        self.user_songs = User.objects.filter(user_id='dummy_user').values_list('user_songs', flat=True)

    def test_check_empty(self):
        self.assert_(dbhelper.check_empty(tracks_df=self.test_df1, user_analysed=self.user_songs[0]))