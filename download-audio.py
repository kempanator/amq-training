# download audio or video files from json files from anisongdb.com

import os
import json
import subprocess
import urllib.request
try:
    import eyed3
except ModuleNotFoundError:
    subprocess.Popen(["python", "-m", "pip", "install", "-U", 'eyed3']).wait()
    import eyed3


# return true if a dictionary key exists and has valid data
def valid_key(d, k):
    return k in d and d[k] is not None and d[k].strip() != ""


mode = 'audio'  # audio, video, both
path = ''  # optional custom path
json_path = path + 'json/'
audio_path = path + 'audio/'
video_path = path + 'video/'
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

if not os.path.isdir(json_path):
    os.mkdir(json_path)

for file_name in os.listdir(json_path):
    if file_name[-5:] == '.json':
        json_file = open(json_path + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if not valid_key(x, hq_video_key) and not valid_key(x, mq_video_key) and not valid_key(x, audio_key):
                pass
            else:
                if mode == 'audio' or mode == 'both':
                    if not os.path.isdir(audio_path):
                        os.mkdir(audio_path)
                    if valid_key(x, audio_key) and x[audio_key].endswith('.mp3'):
                        new_file_name = x[audio_key].split("/")[-1]
                        if not os.path.isfile(audio_path + new_file_name):
                            print(new_file_name + ' - ' + x[anime_name_en_key] + ' - ' + x[song_type_key])
                            urllib.request.urlretrieve(x[audio_key], audio_path + new_file_name)
                            id3 = eyed3.load(audio_path + new_file_name)
                            id3.initTag()
                            id3.tag.artist = x[song_artist_key]
                            id3.tag.title = x[song_name_key]
                            id3.tag.comment = x[song_type_key]
                            id3.tag.album = x[anime_name_en_key]
                            id3.tag.save()
                    else:
                        print('Missing mp3: ' + x[anime_name_en_key] + ', ' + x[song_type_key] + ', ' + x[song_artist_key] + ', ' + x[song_name_key])
                if mode == 'video' or mode == 'both':
                    if not os.path.isdir(video_path):
                        os.mkdir(video_path)
                    link = ""
                    if valid_key(x, mq_video_key):
                        link = x[mq_video_key]
                    if valid_key(x, hq_video_key):
                        link = x[hq_video_key]
                    if link.startswith('http'):  # source can be catbox.moe or openings.moe
                        new_file_name = link.split("/")[-1]
                        if not os.path.isfile(video_path + new_file_name):
                            print(new_file_name + ' - ' + x[anime_name_en_key] + ' - ' + x[song_type_key])
                            urllib.request.urlretrieve(link, video_path + new_file_name)
                    else:
                        print('Missing video: ' + x[anime_name_en_key] + ', ' + x[song_type_key] + ', ' + x[song_artist_key] + ', ' + x[song_name_key])

if len(os.listdir(json_path)) == 0:
    print('Error: no json files found')
if os.path.isdir(audio_path):
    print('total songs in audio folder = ' + str(len(os.listdir(audio_path))))
if os.path.isdir(video_path):
    print('total songs in video folder = ' + str(len(os.listdir(video_path))))
