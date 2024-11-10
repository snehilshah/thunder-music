from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag
from mutagen.id3 import ID3
import csv

songs_path = "D:\\UpdateMusic\\oldies\\**\\*.mp3"

songs = glob.glob(songs_path, recursive=True)
songs_data = []
success_count = 0
failed_count = 0


def write_song_data(title, artist, album, lyrics_found):
    global success_count, failed_count, exists_count
    songs_data.append([title, artist, album, lyrics_found])
    if lyrics_found:
        with open('lyrics/oldies/success.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, artist, album, lyrics_found])
        success_count += 1
    else:
        with open('lyrics/oldies/failed.csv', 'a', newline='',  encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, artist, album, lyrics_found])
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

    write_song_data(params['track_name'], params['artist_name'],
                    params['album_name'], flag_exists)

total_songs = success_count + failed_count
print(f"Total songs processed: {total_songs}")
print(f"Successful: {success_count}")
print(f"Failed: {failed_count}")

success_percentage = (success_count / total_songs) * 100
failure_percentage = (failed_count / total_songs) * 100
success_to_failure_ratio = success_count / \
    failed_count if failed_count != 0 else float('inf')
failure_rate = failed_count / total_songs

with open('lyrics/oldies/metrics.txt', 'w', encoding='utf-8') as metrics_file:
    metrics_file.write(f"Total songs processed: {total_songs}\n")
    metrics_file.write(f"Successful: {success_count}\n")
    metrics_file.write(f"Failed: {failed_count}\n")
    metrics_file.write(f"Success Percentage: {success_percentage:.2f}%\n")
    metrics_file.write(f"Failure Percentage: {failure_percentage:.2f}%\n")
    metrics_file.write(f"Success to Failure Ratio: {
                       success_to_failure_ratio:.2f}\n")
    metrics_file.write(f"Failure Rate: {failure_rate:.2f}\n")
