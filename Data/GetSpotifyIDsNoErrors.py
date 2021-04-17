import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import jellyfish

CLIENT_ID = "51891ef3095849e98336d9d0c83c05e9"
CLIENT_SECRET = "d833852dd80b4117b0e020e480f142c6"

client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

#artist = "DPR Live Crush eaJ"
#title = "Jam & Butterfly"
artist = "George Michael"
title = "I Want Your Sex"
#artist = "Manic Street Preachers"
#title = "Ifwhiteamericatoldthetruthforonedayit'sworldwouldfallapart"
#artist = "Ludacris"
#title = "Get Back"
#artist = "Electrovamp"
#title = "I Don't Like The Vibe In The VIP"
#artist = "Lamb"
#title = "Written"
q1 = "artist:"+artist+" track:"+title
q2 = "artist:%"+artist+" track:%"+title
q3 = artist+" "+title


res3 = sp.search(q=q3, type='track', limit=3)

"""if len(res3['tracks']['items']) != 0:
    print(res3['tracks']['items'][0].keys(), "\n")

    print("\nres3", res3)
    for item in res3['tracks']['items']:
        print("Artists:", item['artists'])
        print("Title:", item['name'])
        print("Id:", item['id'])
        print("Similarity to File artist:", jellyfish.levenshtein_distance(item['artists'][0]['name'], artist))
        print("Similarity to File title:", jellyfish.levenshtein_distance(item['name'], title))
else:
    print(res3)"""

# From returned dictionary get items
# Check if items is >= 1
# Check if artists is >= 1
# Check name of artist

# Open dataset file
dataset = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-1870-spotify.csv", "r", encoding="utf-8")
datareader = csv.reader(dataset)
new_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-spotify-ids.csv", "a+", newline='', encoding="utf-8")
datawriter = csv.writer(new_file)
datareader = list(datareader)
cant_find_file = open("C:\\Users\\rasen\\PythonML\\Testing\\Cant-Find.csv", "a+", newline='', encoding="utf-8")
findwriter = csv.writer(cant_find_file)


def search_song(q, artist, title):
    print("Searching for", artist, "-", title)
    result = sp.search(q=q, type='track', limit=5)
    if len(result['tracks']['items']) >= 1:
        id = ""
        i = 0
        pos = -1
        for item in result['tracks']['items']:
            if item['name'].strip().lower() == title.lower() and item['artists'][0]['name'].strip().lower() == artist.lower():
                pos = i
            #print("Item #", i, ":", result['tracks']['items'][i])
            #print("Spotify Title:", item['name'])
            #print("Spotify Artist:",item['artists'][0]['name'])
            #print("Spotify ID:", item['id'], "\n")

            i += 1

        if pos == -1:
            k = 0
            for item in result['tracks']['items']:
                print("Item #", k, ":", result['tracks']['items'][k])
                print("Spotify Title:", item['name'])
                print("Spotify Artist:",item['artists'][0]['name'])
                print("Spotify ID:", item['id'], "\n")

                k += 1
            print("Searching for", artist, "-", title, "\n")
            index = input("Which index? ")
            if index != "n":
                index = int(index)
                return result['tracks']['items'][index]['id']
            else:
                return ""
        else:
            print("Spotify Title:", result['tracks']['items'][pos]['name'])
            print("Spotify Artist:", result['tracks']['items'][pos]['artists'][0]['name'])
            return result['tracks']['items'][pos]['id']

        #index = input("Which index? ")
        #index = int(index)

        #id = result['tracks']['items'][index]['id']

        #ans = input('\nOkay? ')
        #if ans == "y":
        #    return id
        #else:
        #    return ""

    else:
        print("Couldn't find song:", artist, "-", title, "\n")
        cant_find.append([artist, title])
        return ""


cant_find = []

ctr = 0
for i in range(1844, len(datareader)):
    artist = datareader[i][1].strip()
    title = datareader[i][2].strip()
    q = artist + " " + title
    sp_id = search_song(q, artist, title)
    print("Returned:", sp_id, "\n")
    datareader[i][6] = sp_id.strip()
    datawriter.writerow(datareader[i])
    if sp_id == "":
        ctr += 1
        findwriter.writerow(datareader[i])

print("Title/artist not match:", ctr)
print("Number of not found:", len(cant_find))

dataset.close()
cant_find_file.close()