from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import glob
import music_tag
from mutagen.id3 import ID3

songs_path = "D:/UpdateMusic/Tester/*.mp3"

songs = glob.glob(songs_path)


for song in songs:
    has_lyrics = False
    has_synced_lyrics = False
    
    mp3file = MP3(song, ID3=EasyID3)
    music = music_tag.load_file(song)
    tag = ID3(song)
    
    title = mp3file['title'][0]
    
    if title == "Saturday Nights":
        # with open('D:/MyCodes/lyrics/lyrics.txt', 'a') as file:
        song_lyrics = tag.getall("SYLT")
        # print(type(song_lyrics))
        # song_lyrics = music['lyrics']
        music['lyrics'] = song_lyrics[0]
        print(song_lyrics[0].text)
        music.save()
        
        # songs_lyrics = song_lyrics
        # file.write(str(song_lyrics))
    if music['lyrics']:
        has_lyrics = True
    
    if tag.getall("SYLT"):
        has_synced_lyrics = True
    
    output = f"{title} has: lyrics - {has_lyrics} | synced lyrics - {has_synced_lyrics}"
    
    
    with open('D:/MyCodes/lyrics/Found.txt', 'a') as file:
        file.write(output + '\n')
    