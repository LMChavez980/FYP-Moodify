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

# Open Errors file
errors_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-Errors.csv", "r", encoding="utf-8")
errors_reader = csv.reader(errors_file)
errors_list = list(errors_reader)

# Open Original file
original_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyricsOriginal.csv", "r", encoding="utf-8")
original_reader = csv.reader(original_file)
original_list = list(original_reader)

# Put Original index and artist names into dictionary
original_dict = {}
for i in range(1, len(original_list)):
    key = original_list[i][0]
    val = original_list[i][1]
    original_dict[key] = val

print(original_dict)
print("Original dictionary length:", len(original_dict))

# Put Error index into dictionary
errors_dict = {}
for i in range(1, len(errors_list)):
    key = errors_list[i][0]
    val = errors_list[i][1]
    errors_dict[key] = val

print(errors_dict)
print("Errors dictionary length:", len(errors_dict))

# Loop to check for error indexes in original and assign the name
original_keys = original_dict.keys()
for key in errors_dict.keys():
    if key in original_keys:
        print("Changing:", errors_dict[key], "to", original_dict[key])
        errors_dict[key] = original_dict[key]

print("Updated:", errors_dict)
print("Updated errors dictionary length:", len(errors_dict))

# Create updated errors file
# Open file in a+ mode to append and create file
updated_errors_file = open("C:\\Users\\rasen\\PythonML\\Testing\\MoodyLyrics-UpdatedErrors.csv", "a+", newline='', encoding="utf-8")
updated_errors_writer = csv.writer(updated_errors_file)

# Loop through the errors dictionary and errors list and write them to new file
for i in range(1, len(errors_list)):
    print("Before:", errors_list[i][1])
    key = errors_list[i][0]
    errors_list[i][1] = errors_dict[key]
    print("After:", errors_list[i][1])
    updated_errors_writer.writerow(errors_list[i])
    print("Wrote:", errors_list[i], "\n")

errors_file.close()
original_file.close()
updated_errors_file.close()
