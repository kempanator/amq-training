# look for folders within json folder, look for json files and combine their contents into a new json file

import os
import json

path = ''  # optional custom path
json_path = path + 'json/'

if not os.path.isdir(json_path):
    os.mkdir(json_path)
for folder_name in os.listdir(json_path):
    if os.path.isdir(json_path + folder_name):
        combined_data = []
        for file_name in os.listdir(json_path + folder_name):
            if file_name[-5:] == '.json':
                json_file = open(json_path + folder_name + '/' + file_name, 'r', encoding='utf-8')
                data = json.load(json_file)
                json_file.close()
                for item in data:
                    combined_data.append(item)
        if len(combined_data) > 0:
            if os.path.isfile(json_path + folder_name + '.json'):
                print(folder_name + '.json already exists')
            else:
                json_file_new = open(json_path + folder_name + '.json', 'w', encoding='utf-8')
                json.dump(combined_data, json_file_new, indent=None, separators=(',', ':'))
                json_file_new.close()
                print('created ' + folder_name + '.json')