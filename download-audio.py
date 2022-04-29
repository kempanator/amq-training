# download mp3 files from json files from anisongdb.com

import os
import json
import subprocess
import urllib.request
try:
    import eyed3
except ModuleNotFoundError:
    subprocess.Popen(["python", "-m", "pip", "install", "-U", 'eyed3']).wait()
    import eyed3

path = ''  # optional custom path
if not os.path.isdir(path + 'audio'):
    os.mkdir(path + 'audio')

for file_name in os.listdir(path + 'json/'):
    if file_name[-5:] == '.json':
        json_file = open(path + 'json/' + file_name, encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        for x in data:
            if x['sept'] is None and x['quatre'] is None and x['mptrois'] is None:
                pass
            elif x['mptrois'] is not None and 'catbox.moe' in x['mptrois']:
                mp3_file_name = x['mptrois'].split("/")[-1]
                if not os.path.isfile(path + 'audio/' + mp3_file_name):
                    print(mp3_file_name)
                    urllib.request.urlretrieve(x['mptrois'], path + 'audio/' + mp3_file_name)
                    id3 = eyed3.load(path + 'audio/' + mp3_file_name)
                    id3.initTag()
                    id3.tag.artist = x['Artist']
                    id3.tag.title = x['SongName']
                    id3.tag.comment = x['Type']
                    id3.tag.album = x['Anime']
                    id3.tag.save()
            else:
                print('Missing mp3: ' + x['Anime'] + ', ' + x['Type'] + ', ' + x['Artist'] + ', ' + x['SongName'])

print('total songs in audio folder = ' + str(len(os.listdir(path + 'audio/'))))
