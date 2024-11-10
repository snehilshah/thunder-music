from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag
import os

# Check for lrc file in the same directory as the mp3 file
# and add the lyrics to the mp3 file
# The lyrics should be in the lrc file with the same name as the mp3 file

songs_path = "D:\\UpdateMusic\\downloadedDemistify\\demistify\\**\\*.mp3"

songs = glob.glob(songs_path, recursive=True)
print(f"Total songs: {len(songs)}")
print(songs)
failed = []
success = []
success_count = 0

GREEN = '\033[32m'
BRIGHT_MAGENTA = '\033[95m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BRIGHT_RED = '\033[91m'

for song in songs:
    mp3file = MP3(song, ID3=EasyID3)
    music = music_tag.load_file(song)

    base_name = os.path.splitext(song)[0]
    lrc_file = base_name + ".lrc"

    if os.path.exists(lrc_file):
        with open(lrc_file, 'r', encoding='utf-8') as file:
            lyrics = file.read()
    else:
        print(f'{BRIGHT_RED}Failed{RESET}')
        failed.append([song, 'Not Found'])
        continue

    params = {
        'track_name': mp3file['title'][0],
        'artist_name': mp3file['artist'][0],
        'album_name': mp3file['album'][0],
        'duration': mp3file.info.length,
        'lyrics': lyrics
    }

    try:
        synced_lyrics = params['lyrics']
        try:
            music['lyrics'] = synced_lyrics
            music.save()
            success_count += 1
            success.append([success_count, params['track_name']])
            print(f'{GREEN}Success{RESET}')
        except:
            print(f'{BRIGHT_RED}Failed{RESET}')
            failed.append([params['track_name'], 'Failed to save lyrics'])
            print(f'{BRIGHT_RED}Failed{RESET}')
            failed.append([params['track_name'], 'Not Found'])

    except:
        print(f'{BRIGHT_RED}Failed{RESET}')
        failed.append(song)

# Write the failed songs to a file
with open('zotify/lrc-fail.txt', 'a') as file:
    for song in failed:
        file.write(f"{song[0]} - {song[1]}\n")
    file.close()

with open('zotify/lrc-found.txt', 'a') as file:
    for song in success:
        file.write(f"{song[0]} - {song[1]}\n")
    file.close()

print(f"Success: {len(success)}")
print(f"Failed: {len(failed)}")
print(f"Total: {len(songs)}")
