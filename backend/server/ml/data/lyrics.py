import lyricsgenius as lg
from azapi import AZlyrics
from musixmatch import Musixmatch
import re
from requests.exceptions import HTTPError, Timeout
from fuzzywuzzy import fuzz

GENIUS_CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
GENIUS_CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
GENIUS_CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'
MUSIXMATCH_API_KEY = '77a6fdb434976180c2113ea36918734a'

genius = lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.verbose = False
genius.retries = 3
genius.timeout = 8

musixmatch = Musixmatch(MUSIXMATCH_API_KEY)


def genius_lyrics(song_title, song_artist):
    print("Genius")
    try:
        song = genius.search_song(title=song_title, artist=song_artist)

        if song is not None:
            artist = song.artist.replace("’", "'").lower()
            title = song.title.replace("’", "'").lower()
            if fuzz.partial_ratio(song_artist.lower(), artist) > 70 and fuzz.partial_ratio(song_title.lower(), title) > 70:
                lyrics = song.lyrics.replace("\n", "\\n")
                print("Found Lyrics!")
                return lyrics
            else:
                return None

        return None

    except (HTTPError, Timeout) as e:
        return None


def az_lyrics(song_title, song_artist):
    print("AZ Lyrics")
    azlyrics = AZlyrics(search_engine='duckduckgo', accuracy=0.6)
    azlyrics.title = song_title
    azlyrics.artist = song_artist

    lyrics = azlyrics.getLyrics(save=False)

    if lyrics != 0:
        regex = re.compile("[\r\t]")
        regex_headers = re.compile("[\[].*?[\]]")
        lyrics = re.sub(regex, "", lyrics)
        lyrics = re.sub(regex_headers, "", lyrics)
        lyrics = lyrics.replace("\n", "\\n")
        print("Found Lyrics!")
        return lyrics
    else:
        return None


def musixmatch_lyrics(song_title, song_artist):
    print("Musicxmatch")
    match = musixmatch.matcher_lyrics_get(q_track=song_title, q_artist=song_artist)
    if match['message']['header']['status_code'] == 200:
        tail = 75
        head = len(match['message']['body']['lyrics']['lyrics_body'])
        lyrics = match['message']['body']['lyrics']['lyrics_body'][:head - tail]
        print("Found Lyrics!")
        return lyrics
    else:
        return None


def get_lyrics(tracks_dict):

    # 1. Genius 2. AZ Lyrics 3. Musixmatch
    # AZ Lyrics is less picky about titles however can be blocked by browser
    # Genius is sensitive to titles not matching
    # Musixmatch will only return 30% of lyrics - approx. up to the first verse

    tracks_dict["lyrics"] = ""
    lyrics_list = []

    try:
        for i in range(len(tracks_dict['id'])):
            track_name = tracks_dict['name'][i].strip()
            track_artist = tracks_dict['artists'][i].strip()
            print("Search:", track_name, "-", track_artist)

            # Genius
            lyrics = genius_lyrics(track_name, track_artist)

            # if Genius returns with lyrics - add to list
            # else call AZ Lyrics - call Musixmatch if that fails
            # Add empty string if none found
            if lyrics is not None:
                lyrics_list.append(lyrics)
            else:
                # AZ Lyrics
                lyrics = az_lyrics(track_name, track_artist)

                if lyrics is not None:
                    lyrics_list.append(lyrics)
                else:
                    # Musixmatch
                    lyrics = musixmatch_lyrics(track_name, track_artist)

                    if lyrics is not None:
                        lyrics_list.append(lyrics)
                    else:
                        print("Could not find song")
                        lyrics_list.append("")
    except (HTTPError, Timeout) as e:
        print(e.errno)
        print(e.arg[0])
        print(e.arg[1])

    tracks_dict["lyrics"] = lyrics_list

    return tracks_dict

