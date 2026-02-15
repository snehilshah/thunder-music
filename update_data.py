"""
update_data.py - Catalog all songs from D:\\musicRecovery\\UpdateMusic into data/ CSVs.

Reads ID3 tags (title, artist, album) from MP3 files and writes them to:
    data/english.csv, data/hindi.csv, data/lofi.csv,
    data/oldies.csv, data/ringtones.csv, data/youtube.csv

Usage:
    python update_data.py                  # process all categories
    python update_data.py hindi            # process only hindi
    python update_data.py english oldies   # process english and oldies
"""

import os
import sys
import csv
import glob
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# ── Configuration ──────────────────────────────────────────────────────────
MUSIC_ROOT = r"D:\musicRecovery\UpdateMusic"

# Mapping: folder name -> output CSV filename (without .csv)
CATEGORIES = {
    "english":  "english",
    "hindi":    "hindi",
    "lofi":     "lofi",
    "oldies":   "oldies",
    "ringtone": "ringtones",
    "yt-py":    "youtube",
}

# Terminal colours
GREEN = "\033[32m"
RESET = "\033[0m"
BRIGHT_RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"


# ── Helpers ────────────────────────────────────────────────────────────────
def load_existing(csv_path: str) -> set:
    """Return a set of (title, artist) already in the CSV to avoid duplicates."""
    existing = set()
    if not os.path.exists(csv_path):
        return existing
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header
            if len(row) >= 2:
                existing.add((row[0].strip(), row[1].strip()))
    return existing


def process_category(folder: str, csv_name: str):
    songs_path = os.path.join(MUSIC_ROOT, folder, "**", "*.mp3")
    songs = glob.glob(songs_path, recursive=True)

    if not songs:
        print(f"{YELLOW}  No MP3 files found in {songs_path}{RESET}")
        return

    data_csv = f"data/recovered/{csv_name}.csv"
    os.makedirs("data/recovered", exist_ok=True)
    existing = set()  # Fresh write, no duplicate checking

    print(
        f"\n{CYAN}{'='*60}\n  {csv_name.upper()}  ({folder}/)\n"
        f"  {len(songs)} MP3 files found, {len(existing)} already in CSV\n{'='*60}{RESET}"
    )

    new_songs = []
    error_count = 0
    skipped = 0

    for song in songs:
        try:
            mp3file = MP3(song, ID3=EasyID3)
            title = mp3file.get("title", ["Unknown"])[0]
            artist = mp3file.get("artist", ["Unknown"])[0]
            album = mp3file.get("album", ["Unknown"])[0]
        except Exception as e:
            print(f"  {BRIGHT_RED}Error reading {os.path.basename(song)}: {e}{RESET}")
            error_count += 1
            continue

        if (title.strip(), artist.strip()) in existing:
            skipped += 1
            continue

        new_songs.append([title, artist, album])

    # Write to CSV (append mode, add header only if file is new/empty)
    if new_songs:
        write_header = not os.path.exists(data_csv) or os.path.getsize(data_csv) == 0
        with open(data_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Title", "Artist", "Album"])
            for row in new_songs:
                writer.writerow(row)

    print(f"  {GREEN}Added: {len(new_songs)}{RESET}  |  Skipped (duplicate): {skipped}  |  Errors: {error_count}")


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    requested = [c.lower() for c in sys.argv[1:]] if len(sys.argv) > 1 else list(CATEGORIES.keys())

    valid_keys = list(CATEGORIES.keys()) + list(CATEGORIES.values())

    for arg in requested:
        # Allow passing either folder name or csv name
        if arg in CATEGORIES:
            folder, csv_name = arg, CATEGORIES[arg]
        else:
            # reverse lookup by csv name
            match = {v: k for k, v in CATEGORIES.items()}.get(arg)
            if match:
                folder, csv_name = match, arg
            else:
                print(f"{BRIGHT_RED}Unknown category '{arg}'. Choose from: {', '.join(CATEGORIES.keys())}{RESET}")
                continue
        process_category(folder, csv_name)

    print(f"\n{GREEN}Done!{RESET}")
