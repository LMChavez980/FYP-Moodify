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

"""# Open errors file for reading
errors_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors.csv", "r", encoding="utf-8")
errors_reader = csv.reader(errors_file)
errors_list = list(errors_reader)

# Loop to search for songs
for i in range(1, len(errors_list)):
    try:
        title = errors_list[i][2]
        artist = errors_list[i][1]
        song = genius.search_song(title=title, artist=artist)
        if song is not None:
            print("Genius:", song.title, "File:", title)
            print("Genius:", song.artist, "File:", artist)
            song_title = song.title.replace("’", "'")
            song_artist = song.artist.replace("’", "'")
            if song_title.lower() == errors_list[i][2].lower() and song_artist.lower() == errors_list[i][1].lower():
                lyrics = song.lyrics.replace("\n", "\\n")
                print("All equals:", song_title.lower() == errors_list[i][2].lower() and song_artist.lower() == errors_list[i][1].lower())
                print("Just title:", song_title.lower() == errors_list[i][2].lower())
                print("Just artist:", song_artist.lower() == errors_list[i][1].lower())
                print("Lyrics:", lyrics)
                errors_list[i][5] = lyrics
                print(errors_list[i])
            elif song_title.lower() == errors_list[i][2].lower():
                alt_artist = input("Enter alternative artist name: ")
                song = genius.search_song(title=title, artist=alt_artist)
                print("Lyrics:", song.lyrics.replace("\n", "\\n"))
                alt_lyrics = song.lyrics.replace("\n", "\\n")
                errors_list[i][5] = alt_lyrics
                print(errors_list[i])
            elif song_artist.lower() == errors_list[i][1].lower():
                alt_title = input("Enter alternative title: ")
                song = genius.search_song(title=alt_title, artist=artist)
                print("Lyrics:", song.lyrics.replace("\n", "\\n"))
                alt_lyrics = song.lyrics.replace("\n", "\\n")
                errors_list[i][5] = alt_lyrics
                print(errors_list[i])
        else:
            print("Could not find song")
    except (HTTPError, Timeout) as e:
        print(e.errno)
        print(e.arg[0])
        print(e.arg[1])

# Open file for adding lyrics for errors
error_lyrics_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-WithLyrics.csv", "a+", newline='', encoding="utf-8")
error_lyrics_writer = csv.writer(error_lyrics_file)

for j in range(0, len(errors_list)):
    print(errors_list[j])
    error_lyrics_writer.writerow(errors_list[j])

errors_file.close()
error_lyrics_file.close()"""

# Get Lyrics for songs without lyrics
errors_lyrics = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-WithLyrics.csv", "r", encoding="utf-8")
with_lyrics = csv.reader(errors_lyrics)
errors_nolyrics = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-Subset2.csv", "r", encoding="utf-8")
no_lyrics = csv.reader(errors_nolyrics)

with_lyrics = list(with_lyrics)
no_lyrics = list(no_lyrics)

new_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors-Subset.csv", "a+", newline='', encoding="utf-8")
writer = csv.writer(new_file)

manual = []

#str = "I ran from the devil\nHe was on my back From the Blue Ridge Mountains I followed your path I jumped in the river to cleanse my skin Well my skin froze again when the snow came down Still in the dark I cry your name! Jesus won't save your pain Jesus won't save your pain I learned you can't run from the dirt in your past Mistakes don't disperse through the mountain pass Some say it was the wind that dragged me down But I know like a face is what made me drown Still in the dark I cry your name! Jesus won't save your pain Jesus won't save your pain"

#str1 = "What are we supposed to do? Living in a time like this? What's the flipping do? So many people flipping their lids Keep taking the children to the park Don't let them break your poor little heart Don't let no one get you down 'cause your storm don't bring no calm You will be living in raging force you'll be sorry the day you were born When they castrate your arm. you know? Man and woman we have to talk Even if you don't like world war Even if it makes you mad and we ball Sometimes it's lack of understanding And me and you can manage Before we break down and damage Our heart, our heart, and soul. Our body, our heart, and soul..."

#str2 = "Summer madness Summer madness\nSummer madness Summer madness\nSummer madness Summer madness\nSummer madness Summer madness"

#str3 = "It's summertime and the living is easy\nFish are jumping and the cotton is high Your daddy's rich and your mama's good-looking\nHush, little baby don't you cry\nDon't cry, don't cry, don't cry\nNo no no no\nDon't cry, don't cry\nOne of these mornings you're gonna rise up singing\nYou spread your wings and take to the sky\nBut until that morning there is nothing can harm you\nWith your daddy and mommy standing by\nThey are standing by, I know, don't cry\nSummertime, summertime, summertime and the living is, living is easy Fish are, I know the fish are jumping and cotton is so high Your daddy is so, so rich and your mama good- She had to be good-looking So hush, little baby, don't you cry Don't you cry, no no, don't cry No need to cry, don't cry, don't cry Summertime, summertime"

#str4 = "And you remember The sound of the waves From the wood upon which you stood And you remember The sound of the waves From the wood upon which you stood And you used to rush out to greet them With open arms You used to rush out to greet them With open arms Now We know where you'll be at twelve We know where you'll be at four Now We know where you'll be at twelve We know where you'll be at four Walking down To the liquor store Yeah That'll keep you warm now That'll keep you warm now"

for i in range(1, len(no_lyrics)):
    try:
        title = no_lyrics[i][2].strip()
        artist = no_lyrics[i][1].strip()
        correct = "no"
        while correct != "yes":
            song = genius.search_song(title=title, artist=artist)
            if song is not None:
                print("Genius Title:", song.title, "File Title:", title)
                print("Genius Artist:", song.artist, "File Artist:", artist)
                song_title = song.title.replace("’", "'")
                song_artist = song.artist.replace("’", "'")
                lyrics = song.lyrics.replace("\n", "\\n")
                print("Lyrics:", lyrics)
                correct = input("Correct? ")
                if correct == "na":
                    break
                elif correct == "no":
                    title = input("Title: ")
                    artist = input("Artist: ")
                elif correct == "yes":
                    no_lyrics[i][5] = lyrics
            else:
                print("Can't find song", title, "-", artist)
                manual.append(no_lyrics[i])
                break
        writer.writerow(no_lyrics[i])

    except (HTTPError, Timeout) as e:
        print(e.errno)
        print(e.arg[0])
        print(e.arg[1])

for line in manual:
    print(line)

errors_nolyrics.close()
new_file.close()