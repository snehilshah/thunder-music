import syncedlyrics
import glob
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
import glob
import music_tag

GREEN = '\033[32m'
BRIGHT_MAGENTA = '\033[95m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BRIGHT_RED = '\033[91m'
songs = glob.glob("D:/UpdateMusic/Deemix/*.mp3")


for song in songs:
    tag = ID3(song)
    mp3file = MP3(song, ID3=EasyID3)
    music = music_tag.load_file(song)

    if tag.getall("SYLT"):
        print(
            f"{BRIGHT_MAGENTA}{UNDERLINE}{mp3file['title'][0]}{RESET} already has synced lyrics")
        continue
    if music['lyrics']:
        print(
            f"{BRIGHT_MAGENTA}{UNDERLINE}{mp3file['title'][0]}{RESET} already has lyrics")
        continue
    try:
        params = {
            'track_name': mp3file['title'][0],
            'artist_name': mp3file['artist'][0],
            'album_name': mp3file['album'][0],
            'duration': mp3file.info.length
        }
    except:
        print(f"{BRIGHT_RED}No metadata found for {song}{RESET}")
        continue
    print(
        f"Getting lyrics for {BRIGHT_MAGENTA}{UNDERLINE}{params['track_name']}{RESET}")
    lookup = f"[{mp3file['title'][0]}] [{mp3file['artist'][0]}]"
    # print(lookup)
    res = syncedlyrics.search(lookup, enhanced=True)
    # print(res)
    if res:
        print(f"Trying to syave lyrics")
        try:
            music['lyrics'] = res
            music.save()
            print(f'{GREEN}Success{RESET}')
        except:
            print(f'{BRIGHT_RED}Failed{RESET}')
    else:
        print(f'{BRIGHT_RED}No lyrics found{RESET}')
