import lyricsgenius as lg
from azapi import AZlyrics
from musixmatch import Musixmatch
from requests.exceptions import HTTPError, Timeout

GENIUS_CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
GENIUS_CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
GENIUS_CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'
MUSIXMATCH_API_KEY = '77a6fdb434976180c2113ea36918734a'

genius = lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.verbose = False
genius.retries = 3
genius.timeout = 8

def get_lyrics(tracks_dict):

    # 1. AZ Lyrics 2. Genius 3. Musixmatch
    # AZ Lyrics is less picky about titles
    # Genius is sensitive to titles not matching
    # Musixmatch will only return 30% of lyrics - approx. up to the first verse

    tracks_dict["lyrics"] = ""
    tracks_dict["lyric sentiment"] = ""

    try:
        azlyrics = AZlyrics(search_engine='google')



        for


    except (HTTPError, Timeout) as e:


