import requests
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag
import csv
import time

songs_path = "D:\\UpdateMusic\\hindi\\**\\*.mp3"
start = time.time()

songs = glob.glob(songs_path, recursive=True)
link = 'https://lrclib.net/api/get'
songs_data = []
flag_exists = False
success_count = 0
failed_count = 0
exists_count = 0

GREEN = '\033[32m'
BRIGHT_MAGENTA = '\033[95m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
BRIGHT_RED = '\033[91m'


def write_song_data(title, artist, album, lyrics_found, lyrics_status, existed):
    global success_count, failed_count, exists_count
    if existed:
        exists_count += 1
    songs_data.append([title, artist, album, lyrics_status, existed])
    if lyrics_found:
        with open('lyrics/hindi/success.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, artist, album, lyrics_status, existed])
        success_count += 1
    else:
        with open('lyrics/hindi/failed.csv', 'a', newline='',  encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, artist, album, lyrics_status, existed])
        failed_count += 1


for song in songs:
    flag_exists = False
    mp3file = MP3(song, ID3=EasyID3)
    music = music_tag.load_file(song)

    params = {
        'track_name': mp3file['title'][0],
        'artist_name': mp3file['artist'][0],
        'album_name': mp3file['album'][0],
        'duration': mp3file.info.length
    }

    if str(music['lyrics']) != "":
        flag_exists = True
        continue

    try:
        print(
            f"Getting lyrics for {BRIGHT_MAGENTA}{UNDERLINE}{params['track_name']}{RESET}")
        response = requests.get(link, params=params)
        res = response.json()
        if response.status_code == 200:
            if res['instrumental'] == True:
                print(f'{BRIGHT_RED}Failed{RESET}')
                write_song_data(
                    params['track_name'], params['artist_name'], params['album_name'], False, 'Instrumental', flag_exists)
                continue
            synced_lyrics = res['syncedLyrics']
            try:
                music['lyrics'] = synced_lyrics
                music.save()
                write_song_data(
                    params['track_name'], params['artist_name'], params['album_name'], True, 'Success', flag_exists)
                print(f'{GREEN}Success{RESET}')
            except:
                print(f'{BRIGHT_RED}Failed{RESET}')
                write_song_data(
                    params['track_name'], params['artist_name'], params['album_name'], False, 'Failed to save lyrics', flag_exists)
        elif response.status_code == 404:
            print(f'{BRIGHT_RED}Failed{RESET}')
            write_song_data(
                params['track_name'], params['artist_name'], params['album_name'], False, 'Not Found', flag_exists)

    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        print(f'{BRIGHT_RED}Failed{RESET}')
        write_song_data(
            params['track_name'], params['artist_name'], params['album_name'], False, 'Failed to write', flag_exists)


# Write the songs_data to csv file

with open('data/hindi.csv', 'a', newline='\n',  encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Artist', 'Album', 'Lyrics Status'])
    for song in songs_data:
        writer.writerow(song)

# Show metrics for all successful and failed songs and total songs then write to a file
total_songs = success_count + failed_count + exists_count
success_count = success_count + exists_count
print(f"Total songs processed: {total_songs}")
print(f"Successful: {success_count}")
print(f"Failed: {failed_count}")
print(f"Already existed: {exists_count}")

success_percentage = (success_count / total_songs) * 100
failure_percentage = (failed_count / total_songs) * 100
success_to_failure_ratio = success_count / \
    failed_count if failed_count != 0 else float('inf')
failure_rate = failed_count / total_songs

end = time.time()
total_time = end - start
average_time = total_time / total_songs
total_time_formatted = time.strftime("%H:%M:%S", time.gmtime(total_time))
with open('lyrics/hindi/metrics.txt', 'w', encoding='utf-8') as metrics_file:
    metrics_file.write(f"Total songs processed: {total_songs}\n")
    metrics_file.write(f"Successful: {success_count}\n")
    metrics_file.write(f"Failed: {failed_count}\n")
    metrics_file.write(f"Already existed: {exists_count}\n")
    metrics_file.write(f"Success Percentage: {success_percentage:.2f}%\n")
    metrics_file.write(f"Failure Percentage: {failure_percentage:.2f}%\n")
    metrics_file.write(f"Success to Failure Ratio: {
                       success_to_failure_ratio:.2f}\n")
    metrics_file.write(f"Failure Rate: {failure_rate:.2f}\n")
    metrics_file.write(f"Total Time for {total_songs}: {
                       total_time_formatted}\n")
    metrics_file.write(f"Average Time per Song: {average_time}\n")
