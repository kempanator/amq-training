# convert json files from anisongdb.com into js dictionary
# {listname: [["videolink" "audiolink", "anime", "type", "artist", "song"], ...]}

import os
import json


# return true if a dictionary key exists and has valid data
def valid_key(d, k):
    if k in d and d[k] is not None and d[k].strip() != "":
        return True
    else:
        return False


path = ''  # optional custom path
key_720 = 'sept'
key_480 = 'quatre'
key_mp3 = 'mptrois'
key_anime = 'Anime'
key_type = 'Type'
key_artist = 'Artist'
key_song = 'SongName'
dictionary = {}
total_songs = 0
if not os.path.isdir(path + 'json'):
    os.mkdir(path + 'json')

for file_name in os.listdir(path + 'json/'):
    if file_name[-5:] == '.json':
        list_name = file_name[:-5]
        song_list = []
        json_file = open(path + 'json/' + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if not valid_key(x, key_720) and not valid_key(x, key_480) and not valid_key(x, key_mp3):
                pass
            elif valid_key(x, key_mp3) and x[key_mp3].endswith('.mp3'):
                video = ""
                if valid_key(x, key_480):
                    video = x[key_480]
                if valid_key(x, key_720):
                    video = x[key_720]
                if video == "":
                    print('Missing video: ' + x[key_anime] + ', ' + x[key_type] + ', ' + x[key_artist] + ', ' + x[key_song])
                audio = x[key_mp3]
                anime = x[key_anime].replace('"', '')
                type = x[key_type]
                artist = x[key_artist].replace('"', '')
                song = x[key_song].replace('"', '')
                song_list.append((video, audio, anime, type, artist, song))
                total_songs += 1
            else:
                print('Missing mp3: ' + x[key_anime] + ', ' + x[key_type] + ', ' + x[key_artist] + ', ' + x[key_song])
        song_list = sorted(set(song_list), key=lambda i: str(i[2] + ' ' + i[3]).lower())  # remove duplicates and sort
        dictionary.update({list_name: song_list})

total_lists = len(dictionary)
if total_lists == 0:
    print('Error: nothing found')
else:
    print('total lists = ' + str(total_lists))
    print('total songs = ' + str(total_songs))
    database_file = open(path + 'database.js', 'w', encoding='utf-8')
    database_file.write('let database = ' + json.dumps(dictionary))
    database_file.close()
