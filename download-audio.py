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

mode = 'audio'  # audio, video, both
path = ''  # optional custom path
json_path = path + 'json/'
audio_path = path + 'audio/'
video_path = path + 'video/'

for file_name in os.listdir(json_path):
    if file_name[-5:] == '.json':
        json_file = open(json_path + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if x['sept'] is None and x['quatre'] is None and x['mptrois'] is None:
                pass
            else:
                if mode == 'audio' or mode == 'both':
                    if not os.path.isdir(audio_path):
                        os.mkdir(audio_path)
                    if x['mptrois'] is not None and 'catbox.moe' in x['mptrois']:
                        new_file_name = x['mptrois'].split("/")[-1]
                        if not os.path.isfile(audio_path + new_file_name):
                            print(new_file_name)
                            urllib.request.urlretrieve(x['mptrois'], audio_path + new_file_name)
                            id3 = eyed3.load(audio_path + new_file_name)
                            id3.initTag()
                            id3.tag.artist = x['Artist']
                            id3.tag.title = x['SongName']
                            id3.tag.comment = x['Type']
                            id3.tag.album = x['Anime']
                            id3.tag.save()
                    else:
                        print('Missing mp3: ' + x['Anime'] + ', ' + x['Type'] + ', ' + x['Artist'] + ', ' + x['SongName'])
                if mode == 'video' or mode == 'both':
                    if not os.path.isdir(video_path):
                        os.mkdir(video_path)
                    link = ""
                    if x['quatre'] is not None:
                        link = x['quatre']
                    if x['sept'] is not None:
                        link = x['sept']
                    if link.startswith('http'):  # source can be catbox.moe or openings.moe
                        new_file_name = link.split("/")[-1]
                        if not os.path.isfile(video_path + new_file_name):
                            print(new_file_name)
                            urllib.request.urlretrieve(link, video_path + new_file_name)
                    else:
                        print('Missing video: ' + x['Anime'] + ', ' + x['Type'] + ', ' + x['Artist'] + ', ' + x['SongName'])

if os.path.isdir(audio_path):
    print('total songs in audio folder = ' + str(len(os.listdir(audio_path))))
if os.path.isdir(video_path):
    print('total songs in video folder = ' + str(len(os.listdir(video_path))))
