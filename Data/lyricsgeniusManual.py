# Program will Add lyrics to all errored songs

import lyricsgenius as lg
from requests.exceptions import HTTPError, Timeout
from azapi import AZlyrics
import re
import csv

CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'

genius = lg.Genius(CLIENT_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.verbose = True
genius.retries = 3
genius.timeout = 8

# Readers
rfile = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-Subset2.csv", "r", encoding="utf-8")
reader = csv.reader(rfile)
reader = list(reader)
r2file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-ManualAdds.csv", "r", encoding="utf-8")
reader2 = csv.reader(r2file)
reader2 = list(reader2)
r3file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-Subset.csv", "r", encoding="utf-8")
reader3 = csv.reader(r3file)
reader3 = list(reader3)
r4file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-WithLyrics.csv", "r", encoding="utf-8")
reader4 = csv.reader(r4file)
reader4 = list(reader4)

# Writers
file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-Full.csv", "a+", newline='', encoding="utf-8")
writer = csv.writer(file)

flip_ya_lid_1230 = 'What are we supposed to do?\\nLiving in a time like this?\\nWhat\'s the flipping do?\\nSo many people ' \
              'flipping their lids\\nKeep taking the children to the park\\nDon\'t let them break your poor little ' \
              'heart\\nDon\'t let no one get you down\\n\'Cause your storm don\'t bring no calm\\nYou will be living in ' \
              'raging force\\nYou\'ll be sorry the day you were born\\nWhen they castrate your arm\\nYou know, ' \
              'man and woman, we have to talk\\nEven if you don\'t like world war\\nEven if it makes you mad and we ' \
              'ball\\nSometimes it\'s lack of understanding\\nAnd me and you can manage\\nBefore we break down and ' \
              'damage\\nOur heart, our heart and soul\\nOur body, our heart and soul\\nDon\'t flip your lids\\nDon\'t lose ' \
              'it\\nDon\'t flip your lids\\nDon\'t lose it\\nDon\'t flip your lids\\nOh-oh-oh, it\'s alright\\nOh-oh-oh, ' \
              'it\'s alright'

rivulets_1869 = 'And you remember\\nThe sound of the waves\\nFrom the wood upon which you stood\\nAnd you remember\\nThe ' \
           'sound of the waves\\nFrom the wood upon which you stood\\nAnd you used to rush out to greet them\\nWith ' \
           'open arms\\nYou used to rush out to greet them\\nWith open arms\\nNow\\nWe know where you\'ll be at ' \
           'twelve\\nWe know where you\'ll be at four\\nNow\\nWe know where you\'ll be at twelve\\nWe know where ' \
           'you\'ll be at four\\nWalking down\\nTo the liquor store\\nYeah\\nThat\'ll keep you warm now\\nThat\'ll ' \
           'keep you warm now'

#writer.writerow(['ML1230', flip_ya_lid_1230])
#writer.writerow(['ML1869', rivulets_1869])

# Get keys of manual errors
manual = {}
for i in range(0, len(reader2)):
    key = reader2[i][0]
    val = reader2[i][1]
    manual[key] = val

print(manual)

# Get lyrics of error subset 2 (No lyrics on Genius)
errors = {}
for i in range(1, len(reader)):
    key = reader[i][0].strip()
    val = reader[i][5].strip()
    print(reader[i][2].strip())
    print(reader[i][1].strip())
    if key not in manual.keys():
        title = input("Enter Title: ")
        artist = input("Enter Artist: ")
        song = genius.search_song(title=title, artist=artist)
        if song is not None:
            gTitle = song.title.strip()
            gArtist = song.artist.strip()
            print("Genius Title:", gTitle)
            print("Genius Artist:", gArtist)
            lyrics = song.lyrics.replace("\n", "\\n")
            print("Lyric:", lyrics)
            errors[key] = lyrics
    else:
        print("Song is manual addition")
        errors[key] = manual[key]
        print(errors[key])

print(errors)

# Get dictionary of all errored songs in subset 1 (Name Errors) with lyrics
errors_s1 = {}
for i in range(0, len(reader3)):
    key = reader3[i][0].strip()
    val = reader3[i][5].strip()
    errors_s1[key] = val
    if key in errors.keys():
        errors_s1[key] = errors[key]

print(errors_s1)

# Get dictionary of all errored songs
errors_with_lyrics = {}
for i in range(1, len(reader4)):
    key = reader4[i][0].strip()
    val = reader4[i][5].strip()
    errors_with_lyrics[key] = val
    if key in errors_s1.keys():
        errors_with_lyrics[key] = errors_s1[key]
    reader4[i][5] = errors_with_lyrics[key]
    writer.writerow(reader4[i])

for key, val in errors_with_lyrics.items():
    print(key, ":", val)

print(len(errors_with_lyrics.keys()))
print(len(reader4))


file.close()
rfile.close()
r2file.close()
r3file.close()
