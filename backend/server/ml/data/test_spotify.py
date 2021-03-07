from unittest import TestCase
from ml.data import spotify

class Test(TestCase):
    def test_create_playlist(self):
        assert spotify.create_playlist(userid="lmchavez", mood="Relax", tracks=[])

