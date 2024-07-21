import requests
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag

songs_path = "D:/UpdateMusic/Deemix/*.mp3"

songs = glob.glob("D:/UpdateMusic/English/*.mp3")
link = 'https://lrclib.net/api/get'
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

    params = {
        'track_name': mp3file['title'][0],
        'artist_name': mp3file['artist'][0],
        'album_name': mp3file['album'][0],
        'duration': mp3file.info.length
    }

    try:
        print(
            f"Getting lyrics for {BRIGHT_MAGENTA}{UNDERLINE}{params['track_name']}{RESET}")
        response = requests.get(link, params=params)
        res = response.json()
        if response.status_code == 200:
            if res['instrumental'] == True:
                print(f'{BRIGHT_RED}Failed{RESET}')
                failed.append([params['track_name'], 'Instrumental'])
                continue
            synced_lyrics = res['syncedLyrics']
            try:
                music['lyrics'] = synced_lyrics
                music.save()
                success_count += 1
                success.append([success_count, params['track_name']])
                print(f'{GREEN}Success{RESET}')
            except:
                print(f'{BRIGHT_RED}Failed{RESET}')
                failed.append([params['track_name'], 'Failed to save lyrics'])
        elif response.status_code == 404:
            print(f'{BRIGHT_RED}Failed{RESET}')
            failed.append([params['track_name'], 'Not Found'])

    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        print(f'{BRIGHT_RED}Failed{RESET}')
        failed.append(
            [params['track_name'], requests.exceptions.RequestException])

# Write the failed songs to a file
with open('D:/MyCodes/lyrics/new_failed_songs.txt', 'a') as file:
    for song in failed:
        file.write(f"{song[0]} - {song[1]}\n")
    file.close()

with open('D:/MyCodes/lyrics/new_success_songs.txt', 'a') as file:
    for song in success:
        file.write(f"{song[0]} - {song[1]}\n")
    file.close()
