import lyricsgenius as lg
from azapi import AZlyrics
import re
import csv
from musixmatch import Musixmatch

GENIUS_CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
GENIUS_CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
GENIUS_CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'
MUSIXMATCH_API_KEY = '77a6fdb434976180c2113ea36918734a'