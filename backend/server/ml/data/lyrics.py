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

def get_lyrics(tracks_dict):

    # 1. AZ Lyrics 2. Genius 3. Musixmatch
    # AZ Lyrics is less picky about titles
    # Genius is sensitive to titles not matching
    # Musixmatch will only return 30% of lyrics - approx. up to the first verse

    tracks_dict["lyrics"] = ""
    lyrics_list = []
    lyrics_unavailable = []

    try:
        method = 1
        azlyrics = AZlyrics(search_engine='duckduckgo')

        for i in range(len(tracks_dict['id'])):
            track_name = tracks_dict['name'][i]
            track_artist = tracks_dict['artists'][i]
            print("Search:", track_name, "-", track_artist)
            azlyrics.title = track_name
            azlyrics.artist = track_artist

            res_lyrics = azlyrics.getLyrics(save=False)

            # If there is a valid result
            if res_lyrics != 0:
                print("AZ Lyrics")
                regex = re.compile("[\r\t]")
                regex_headers = re.compile("[\[].*?[\]]")
                res_lyrics = re.sub(regex, "", res_lyrics)
                res_lyrics = re.sub(regex_headers, "", res_lyrics)
                lyrics = res_lyrics.replace("\n", "\\n")
                lyrics_list.append(lyrics)
            else:
                method = 2
                song = genius.search_song(title=track_name, artist=track_artist)

                if song is not None:
                    print("Genius Lyrics")
                    artist = song.artist.replace("’", "'").lower()
                    title = song.title.replace("’", "'").lower()
                    print(title, "-",artist)
                    if fuzz.partial_ratio(track_artist.lower(), artist) > 70 and fuzz.partial_ratio(track_name.lower(), title) > 70:
                        lyrics = song.lyrics.replace("\n", "\\n")
                        lyrics_list.append(lyrics)
                    else:
                        method = 3
                        print("Musixmatch Lyrics")
                        ret = lyrics_musixmatch(track_name, track_artist)
                        if ret != "":
                            lyrics_list.append(ret)
                        else:
                            lyrics_list.append("")
                else:
                    method = 3
                    print("Musixmatch Lyrics")
                    ret = lyrics_musixmatch(track_name, track_artist)
                    if ret != "":
                        lyrics_list.append(ret)
                    else:
                        lyrics_list.append("")

    except (HTTPError, Timeout) as e:
        print(e.errno)
        print(e.arg[0])
        print(e.arg[1])

    tracks_dict["lyrics"] = lyrics_list

    return tracks_dict


def lyrics_musixmatch(title, artist):
    match = musixmatch.matcher_lyrics_get(q_track=title, q_artist=artist)
    if match['message']['header']['status_code'] == 200:
        tail = 75
        head = len(match['message']['body']['lyrics']['lyrics_body'])
        lyrics = match['message']['body']['lyrics']['lyrics_body'][:head - tail]

        return lyrics
    else:
        print("Couldn't find song")
        return ""
