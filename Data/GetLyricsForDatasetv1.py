import lyricsgenius as lg
from requests.exceptions import HTTPError, Timeout
from azapi import AZlyrics
import re
import csv
from musixmatch import Musixmatch

CLIENT_ID = '18H6V8QvCrj0kKOefOVWUkkIowkMI84kEv8mK9N01fC_D7ALSIC3PPbbYZoN0vu1'
CLIENT_SECRET = '187PZ_Um5c3EOZm4rWV8toxjMlzZ84sZfJKhM_D8b4VAhVzXuI1m9TTX49Jrdq7Ysy5s5htzvpCiOAv1RIqQvw'
CLIENT_ACCESS_TOKEN = 'WdcEvFz0MeZOgDNtrRfAmJ0DReEqv8_MdSwTmQBCBCZCizR5Pf1P7dgfnzKdrOGB'

genius = lg.Genius(CLIENT_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.verbose = True
genius.retries = 3
genius.timeout = 8

# Open files
# Open dataset for reading
moody_dataset = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Sentiment-Lyrics-CSV.csv", "r", encoding="utf-8")
# Open file for writing: New csv with lyrics
lyrics_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Sentiment-WithLyrics-CSV.csv", "a+", newline='', encoding="utf-8")
# CSV readers and writers
reader = csv.reader(moody_dataset)
writer = csv.writer(lyrics_file)
# Open file for writing: Song with issues getting lyrics
errors_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors.csv", "a+", newline='', encoding="utf-8")
error_writer = csv.writer(errors_file)

no_lyrics = []

moody_rows = list(reader)

for i in range(0, len(moody_rows)):
    if i == 0:
        writer.writerow(moody_rows[0])
        print("Wrote Labels")
    else:
        try:
            song = genius.search_song(title=moody_rows[i][2], artist=moody_rows[i][1])
            if song is None:
                print("Adding "+moody_rows[i][2]+" - "+moody_rows[i][1]+" to no_lyrics list - Cannot find song")
                no_lyrics.append(moody_rows[i])
                writer.writerow(moody_rows[i])
                error_writer.writerow(moody_rows[i])
            else:
                artist = song.artist.replace("’", "'").lower()
                print(artist)
                title = song.title.replace("’", "'").lower()
                print(title)
                if artist == moody_rows[i][1].lower() and title == moody_rows[i][2].lower():
                    lyrics = song.lyrics.replace("\n", "\\n")
                    moody_rows[i][3] = lyrics
                    print(moody_rows[i][3])
                    writer.writerow(moody_rows[i])
                else:
                    print("Adding " + moody_rows[i][2] + " - " + moody_rows[i][1] + " to no_lyrics list - Title or Artist issue")
                    no_lyrics.append(moody_rows[i])
                    writer.writerow(moody_rows[i])
                    error_writer.writerow(moody_rows[i])

        except (HTTPError, Timeout) as e:
            print(e.errno)
            print(e.arg[0])
            print(e.arg[1])
            print("i value: "+i)

for line in no_lyrics:
    print(line)
    print("Wrote "+line[0]+"-"+line[2]+"-"+line[1])


#song = genius.search_song("I Keed", "Triumph the Insult Comic Dog")
#print(song.title)
#print(song.artist)
#print(song.lyrics.replace("\n", " "))


#str = "I ran from the devil He was on my back From the Blue Ridge Mountains I followed your path I jumped in the river to cleanse my skin Well my skin froze again when the snow came down Still in the dark I cry your name! Jesus won't save your pain Jesus won't save your pain I learned you can't run from the dirt in your past Mistakes don't disperse through the mountain pass Some say it was the wind that dragged me down But I know like a face is what made me drown Still in the dark I cry your name! Jesus won't save your pain Jesus won't save your pain"

#str1 = "What are we supposed to do? Living in a time like this? What's the flipping do? So many people flipping their lids Keep taking the children to the park Don't let them break your poor little heart Don't let no one get you down 'cause your storm don't bring no calm You will be living in raging force you'll be sorry the day you were born When they castrate your arm. you know? Man and woman we have to talk Even if you don't like world war Even if it makes you mad and we ball Sometimes it's lack of understanding And me and you can manage Before we break down and damage Our heart, our heart, and soul. Our body, our heart, and soul..."

#str2 = "Summer madness Summer madness Summer madness Summer madness Summer madness Summer madness Summer madness Summer madness"

str3 = "It's summertime and the living is easy Fish are jumping and the cotton is high Your daddy's rich and your mama's good-looking Hush, little baby don't you cry Don't cry, don't cry, don't cry No no no no Don't cry, don't cry One of these mornings you're gonna rise up singing You spread your wings and take to the sky But until that morning there is nothing can harm you With your daddy and mommy standing by They are standing by, I know, don't cry Summertime, summertime, summertime and the living is, living is easy Fish are, I know the fish are jumping and cotton is so high Your daddy is so, so rich and your mama good- She had to be good-looking So hush, little baby, don't you cry Don't you cry, no no, don't cry No need to cry, don't cry, don't cry Summertime, summertime"

str4 = "And you remember The sound of the waves From the wood upon which you stood And you remember The sound of the waves From the wood upon which you stood And you used to rush out to greet them With open arms You used to rush out to greet them With open arms Now We know where you'll be at twelve We know where you'll be at four Now We know where you'll be at twelve We know where you'll be at four Walking down To the liquor store Yeah That'll keep you warm now That'll keep you warm now"

#print(str4)

#print(str.replace("\n", " "))

"""lyrics_file = open('C:\\Users\\rasen\\Documents\\MoodyLyricsFull4-UTF.csv', 'r', encoding="utf-8")
reader = csv.reader(lyrics_file)
rows = list(reader)

str1 = rows[1734][3]
stren = str1.encode('utf-8')
strde = stren.decode('cp1252')
print(stren)
print(strde)
#for i in range(1, 5):
#    print(rows[i][0]+":"+rows[i][3])

#for i in range(1, len(rows)):
#    print(rows[i])

lyrics_file.close()"""

#lyrics = re.sub("[\(\[].*?[\)\]]", "", song.lyrics)

#print('AZLyrics API')

#azlyrics = AZlyrics(search_engine='google')

#azlyrics.artist = "Wu-Tang Clan"
#azlyrics.title = "Wu-Tang Clan Ain't Nuthing Ta F' Wit"

#azlyrics.getLyrics(save=False)

#lyrics = re.sub("[\[].*?[\]]", "", azlyrics.lyrics)

#lyrics_nonewline = re.sub("[\r\t]", "", lyrics).strip()

#lyrics_nonewline = lyrics_nonewline.replace("\n", " ")

#print(lyrics_nonewline.replace("\\", ""))

