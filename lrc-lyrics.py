from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag
import os
import csv

# Check for lrc file
# and add the lyrics to the mp3 file
# The lyrics should be in the lrc file with the same name as the mp3 file

songs_path = "D:\\UpdateMusic\\**\\*.mp3"
lrc_path = "D:\\UpdateMusic\\lyrics\\"
csv_file_path = ".\\lyrics\\lrc\\lrc-available.csv"

songs = glob.glob(songs_path, recursive=True)
print(f"Total songs: {len(songs)}")
failed = []
success = []
success_count = 0
successful_entries = []

GREEN = '\033[32m'
BRIGHT_MAGENTA = '\033[95m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BRIGHT_RED = '\033[91m'

for song in songs:
    mp3file = MP3(song, ID3=EasyID3)
    music = music_tag.load_file(song)

    base_name = os.path.splitext(song)[0]
    lrc_file = base_name.split('\\')[-1] + ".lrc"
    lrc_full_path = os.path.join(lrc_path, lrc_file)

    if os.path.exists(lrc_full_path):
        with open(lrc_full_path, 'r', encoding='utf-8') as file:
            lyrics = file.read()
    else:
        failed.append([song.split('-')[-1].strip(), 'File Not Found'])
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
            print(f'{GREEN}Success: {params["track_name"]}{RESET}')

            successful_entries.append(
                [params['track_name'], params['artist_name'], params['album_name']])
        except:
            failed.append([params['track_name'], 'Failed to save lyrics'])

    except:
        failed.append(song)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['title', 'artist', 'album'])
    csvwriter.writerows(successful_entries)

total_songs = len(songs)
total_success = len(success)
total_failed = len(failed)
success_percentage = (total_success / total_songs) * \
    100 if total_songs > 0 else 0
failed_percentage = (total_failed / total_songs) * \
    100 if total_songs > 0 else 0

with open('.\\lyrics\\lrc\\metrics.txt', 'w', encoding='utf-8') as result_file:
    result_file.write(f"Total songs: {total_songs}\n")
    result_file.write(f"Success: {total_success}\n")
    result_file.write(f"Failed: {total_failed}\n")
    result_file.write(f"Success Percentage: {success_percentage:.2f}%\n")
    result_file.write(f"Failed Percentage: {failed_percentage:.2f}%\n")
