import os
import csv
from mutagen.easyid3 import EasyID3

# Check copy of mp3 files based on ID3 tags
# WARNING: The files from `dir1` will be deleted
# if they have the same title, artist, and year as the files in `dir2`

def get_mp3_files(directory):
    mp3_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))
    return mp3_files


def get_mp3_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        title = audio.get('title', ['Unknown'])[0]
        artist = audio.get('artist', ['Unknown'])[0]
        year = audio.get('date', ['Unknown'])[0]
        return title, artist, year
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None


def find_duplicates(dir1, dir2):
    files1 = get_mp3_files(dir1)
    files2 = get_mp3_files(dir2)

    metadata1 = {get_mp3_metadata(f): f for f in files1}
    metadata2 = {get_mp3_metadata(f): f for f in files2}

    duplicates = set(metadata1.keys()) & set(metadata2.keys())

    with open('duplicates.csv', mode='w', newline='') as csv_file, open('deleted_files.txt', mode='w') as txt_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Artist', 'Year', 'File 1', 'File 2'])

        for meta in duplicates:
            writer.writerow([meta[0], meta[1], meta[2],
                            metadata1[meta], metadata2[meta]])
            print(f"Duplicate found: {meta}")
            print(f"File 1: {metadata1[meta]}")
            print(f"File 2: {metadata2[meta]}")
            os.remove(metadata1[meta])
            txt_file.write(f"Deleted: {metadata1[meta]}\n")
            print(f"Deleted: {metadata1[meta]}")


if __name__ == "__main__":
    dir1 = "D:\\UpdateMusic\\Hindi"
    dir2 = "D:\\UpdateMusic\\downloadedDemistify\\demistify"

    find_duplicates(dir1, dir2)
