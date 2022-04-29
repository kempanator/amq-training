# convert json files from anisongdb.com into js dictionary
# {listname: [["link", "anime", "type", "artist", "song"], ...]}

import os
import json

path = ''  # optional custom path
if not os.path.isdir(path + 'json'):
    os.mkdir(path + 'json')
dictionary = {}
total_songs = 0

for file_name in os.listdir(path + 'json/'):
    if file_name[-5:] == '.json':
        list_name = file_name[:-5]
        song_list = []
        json_file = open(path + 'json/' + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if x['sept'] is None and x['quatre'] is None and x['mptrois'] is None:
                pass
            elif x['mptrois'] is not None and 'catbox.moe' in x['mptrois']:
                video = ""
                if x['quatre'] is not None:
                    video = x['quatre']
                if x['sept'] is not None:
                    video = x['sept']
                audio = x['mptrois']
                anime = x['Anime'].replace('"', '')
                type = x['Type']
                artist = x['Artist'].replace('"', '')
                song = x['SongName'].replace('"', '')
                song_list.append((video, audio, anime, type, artist, song))
                total_songs += 1
            else:
                print('Missing mp3: ' + x['Anime'] + ', ' + x['Type'] + ', ' + x['Artist'] + ', ' + x['SongName'])
        song_list = sorted(set(song_list), key=lambda i: i[1] + ' ' + i[2])  # remove duplicates and sort
        dictionary.update({list_name: song_list})

total_lists = len(dictionary)
if total_lists == 0:
    print('error: nothing found')
else:
    print('total lists = ' + str(total_lists))
    print('total songs = ' + str(total_songs))
    database_file = open(path + 'database.js', 'w', encoding='utf-8')
    database_file.write('let database = ' + json.dumps(dictionary))
    database_file.close()
