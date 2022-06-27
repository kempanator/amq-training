# amq-training

A local webpage for practicing matching anime songs to their series. This program reads anisongdb json files and creates a randomized song list that you listen to and click through with arrow buttons. The anime, artist, and song names are hidden until you click the result button.

## How to Download
1. click green code button
2. download zip
3. open zip
4. copy inside folder
5. paste somewhere
6. open index.html

## Adding new lists
1. download json file from https://anisongdb.com
2. rename json file to whatever you want the list name to be called
3. place json file in json folder
4. run update-database.py

## Downloading lists
Running download-audio.py will create an audio folder and fill it with mp3 files of every song from every json file. The webpage will automatically try to use local files first then try the url.

## Merging Lists
1. create a new folder in json folder with the new list name
2. add json files to this folder
3. run merge-json.py
4. merged json file will be created in json folder