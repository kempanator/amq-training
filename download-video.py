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
    if k in d and d[k] is not None and d[k].strip() != "":
        return True
    else:
        return False


mode = 'video'  # audio, video, both
path = ''  # optional custom path
json_path = path + 'json/'
audio_path = path + 'audio/'
video_path = path + 'video/'
key_720 = 'sept'
key_480 = 'quatre'
key_mp3 = 'mptrois'
key_anime = 'Anime'
key_type = 'Type'
key_artist = 'Artist'
key_song = 'SongName'
if not os.path.isdir(json_path):
    os.mkdir(json_path)

for file_name in os.listdir(json_path):
    if file_name[-5:] == '.json':
        json_file = open(json_path + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if not valid_key(x, key_720) and not valid_key(x, key_480) and not valid_key(x, key_mp3):
                pass
            else:
                if mode == 'audio' or mode == 'both':
                    if not os.path.isdir(audio_path):
                        os.mkdir(audio_path)
                    if valid_key(x, key_mp3) and x[key_mp3].endswith('.mp3'):
                        new_file_name = x[key_mp3].split("/")[-1]
                        if not os.path.isfile(audio_path + new_file_name):
                            print(new_file_name + ' - ' + x[key_anime] + ' - ' + x[key_type])
                            urllib.request.urlretrieve(x[key_mp3], audio_path + new_file_name)
                            id3 = eyed3.load(audio_path + new_file_name)
                            id3.initTag()
                            id3.tag.artist = x[key_artist]
                            id3.tag.title = x[key_song]
                            id3.tag.comment = x[key_type]
                            id3.tag.album = x[key_anime]
                            id3.tag.save()
                    else:
                        print('Missing mp3: ' + x[key_anime] + ', ' + x[key_type] + ', ' + x[key_artist] + ', ' + x[key_song])
                if mode == 'video' or mode == 'both':
                    if not os.path.isdir(video_path):
                        os.mkdir(video_path)
                    link = ""
                    if valid_key(x, key_480):
                        link = x[key_480]
                    if valid_key(x, key_720):
                        link = x[key_720]
                    if link.startswith('http'):  # source can be catbox.moe or openings.moe
                        new_file_name = link.split("/")[-1]
                        if not os.path.isfile(video_path + new_file_name):
                            print(new_file_name + ' - ' + x[key_anime] + ' - ' + x[key_type])
                            urllib.request.urlretrieve(link, video_path + new_file_name)
                    else:
                        print('Missing video: ' + x[key_anime] + ', ' + x[key_type] + ', ' + x[key_artist] + ', ' + x[key_song])

if len(os.listdir(json_path)) == 0:
    print('Error: no json files found')
if os.path.isdir(audio_path):
    print('total songs in audio folder = ' + str(len(os.listdir(audio_path))))
if os.path.isdir(video_path):
    print('total songs in video folder = ' + str(len(os.listdir(video_path))))
