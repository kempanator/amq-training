# convert json files from anisongdb.com into js dictionary
# {listname: [["video_link", "audio_link", "anime_name_en", "anime_name_jp", "anime_type", "anime_vintage", "song_artist", "song_name", "song_type", "song_difficulty"], ...]}

import os
import json


# return true if a dictionary key exists and has valid data
def valid_key(d, k):
    return k in d and d[k] is not None and d[k].strip() != ""


path = ''  # optional custom path
hq_video_key = 'HQ'
mq_video_key = 'MQ'
audio_key = 'audio'
anime_name_expand_key = 'animeExpandName'
anime_name_en_key = 'animeENName'
anime_name_jp_key = 'animeJPName'
anime_type_key = 'animeType'
anime_vintage_key = 'animeVintage'
song_artist_key = 'songArtist'
song_name_key = 'songName'
song_type_key = 'songType'
song_difficulty_key = 'songDifficulty'
ann_id_key = 'annId'
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
            if not valid_key(x, hq_video_key) and not valid_key(x, mq_video_key) and not valid_key(x, audio_key):
                pass
            elif valid_key(x, audio_key) and x[audio_key].endswith('.mp3'):
                video = ""
                if valid_key(x, mq_video_key):
                    video = x[mq_video_key]
                if valid_key(x, hq_video_key):
                    video = x[hq_video_key]
                if video == "":
                    print('Missing video: ' + str(x))
                audio = x[audio_key]
                anime_name_en = x[anime_name_en_key].replace('"', '')
                anime_name_jp = x[anime_name_jp_key].replace('"', '')
                anime_type = x[anime_type_key]
                anime_vintage = x[anime_vintage_key]
                song_artist = x[song_artist_key].replace('"', '')
                song_name = x[song_name_key].replace('"', '')
                song_type = x[song_type_key]
                song_difficulty = x[song_difficulty_key]
                song_list.append((video, audio, anime_name_en, anime_name_jp, anime_type, anime_vintage, song_artist, song_name, song_type, song_difficulty))
                total_songs += 1
            else:
                print('Missing mp3: ' + str(x))
        song_list = sorted(set(song_list), key=lambda i: str(i[2] + ' ' + i[3]).lower())  # remove duplicates and sort
        dictionary.update({list_name: song_list})

total_lists = len(dictionary)
if total_lists == 0:
    print('error: nothing found')
else:
    print('total lists = ' + str(total_lists))
    print('total songs = ' + str(total_songs))
    database_file = open(path + 'database.js', 'w', encoding='utf-8')
    database_file.write('let database = ' + json.dumps(dictionary, indent=None, separators=(',', ':')))
    database_file.close()
