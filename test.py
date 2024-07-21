
from mutagen.id3 import ID3, SYLT, Encoding
import requests
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, SYLT, Encoding

import glob
import music_tag

GREEN = '\033[32m'
BRIGHT_MAGENTA = '\033[95m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BRIGHT_RED = '\033[91m'

songs = glob.glob("D:/UpdateMusic/temp/*.mp3")

for song in songs:
    # mp3file = MP3(song, ID3=EasyID3)
    # music = music_tag.load_file(song)

    # params = {
    #     'track_name': mp3file['title'][0],
    #     'artist_name': mp3file['artist'][0],
    #     'album_name': mp3file['album'][0],
    #     'duration': mp3file.info.length
    # }

    # if music['SYLT']:
    #     print(
    #         f"{BRIGHT_MAGENTA}{UNDERLINE}{mp3file['title'][0]}{RESET}")
    # else:
    #     print(
    #         f"{BRIGHT_RED}{UNDERLINE}{mp3file['title'][0]}{RESET}")



    tag = ID3(song)
    # tag.setall("SYLT", [SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=sync_lrc)])
    print(tag.getall("SYLT"))
