import lyricsgenius as lg
from azapi import AZlyrics
import re
from fuzzywuzzy import fuzz
import csv
from musixmatch import Musixmatch


def get_lyrics(playlist_dict):
    playlist_songs = playlist_dict

    for playlist_id in playlist_songs.keys():
        for song in playlist_songs[playlist_id]:
            print(0)

GENIUS_CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
GENIUS_CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
GENIUS_CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'
MUSIXMATCH_API_KEY = '77a6fdb434976180c2113ea36918734a'

genius = lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.retries = 3
genius.timeout = 10

song = genius.search_song(title="I Luv Ya", artist="Young Jeezy & Busta Rhymes")

if song is not None:
    print(fuzz.ratio("Young Jeezy & Busta Rhymes", song.artist))
    print(song.artist)
    print(fuzz.ratio("I Luv Ya", song.title))
    print(song.title)
    #print(song.lyrics)
else:
    print("No song")

google = 'google'
duckgo = 'duckduckgo'

azlyrics = AZlyrics(search_engine=duckgo)

azlyrics.title = "Wu-Tang Clan Ain't Nuthing Ta F' Wit"
azlyrics.artist = "Wu-Tang Clan"

lyrics_az = azlyrics.getLyrics(save=False)

#print(lyrics_az)

#print(lyrics_az)
regex = re.compile("[\r\t]")
regex_headers = re.compile("[\[].*?[\]]")
lyrics_az = re.sub(regex, "", lyrics_az)
lyrics_az = re.sub(regex_headers, "", lyrics_az)

lyrics = lyrics_az.replace("\n", "\\n")
#lyrics_list = lyrics_az.split('\n')

#print(lyrics_list)

#lyrics = '\\n'.join(lyrics_list).strip()

print(lyrics)


