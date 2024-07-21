# Thunder Synced Lyrics

Thunder Synced Lyrics is a Python script that downloads and adds the lyrics metadata to your music files. I'm using [LRC LIB](https://lrclib.net) to fetch synced lyrics.

## Features:
- Downloads and adds synced lyrics to your music files.
- Supports multiple file formats including mp3, m4a, flac, and more.
- Supports multiple languages including English, Spanish, French, and more.


## To start using Thunder Synced Lyrics:

1. Install the required dependencies by running the following command:
```bash
    pip install -r requirements.txt
```
2. Update the songs_path variable in `synced_lyrics.py` with the path to your music files.
```python
    songs_path = "path/to/your/music/files"
```

3. Run the script by running the following command:
```bash
    python synced_lyrics.py
```


Success Percentage: 93.04%
Failure Percentage: 6.96%
Success to Failure Ratio: 13.37
Failure Rate: 0.07