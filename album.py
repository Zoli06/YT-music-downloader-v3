from multiprocessing import Pool
import os
from song import Song


class Album:
    __slots__ = ("id", "title", "artist", "songs", "thumbnails")
    
    def __init__(self, id: str, title: str, artist: str, songs: list, thumbnails: list):
        self.id = id
        self.title = title
        self.artist = artist
        self.songs = songs
        self.thumbnails = thumbnails
        
    def __str__(self):
        return f"{self.title} by {self.artist} with {len(self.songs)} songs"
    
    @staticmethod
    def get_album(user, id: str):
        data = user.api.get_album(id)
        title = data["title"]
        artist = ', '.join([artist["name"] for artist in data["artists"]])
        songs = []
        thumbnails = data["thumbnails"]
        for song in data["tracks"]:
            if song["videoId"] is not None:
                songs.append(
                    Song(
                        id=song["videoId"],
                        title=song["title"],
                        artist=", ".join([artist["name"]
                                        for artist in song["artists"]]),
                        time=song["duration_seconds"],
                        thumbnails=song["thumbnails"],
                        album=song["album"],
                    )
                )
            else:
                print(f"Skipping {song['title']} because it is unavailable")
        
        return Album(id, title, artist, songs, thumbnails)
    
    def download(self, save_location: str):
        print(f"Downloading {self.title} by {self.artist} with {len(self.songs)} songs")
        
        # Make directory
        save_location = f"{save_location}/{self.title}"
        
        if not os.path.exists(save_location):
            os.mkdir(save_location)
            
        pool = Pool(processes=8)
        
        for song in self.songs:
            pool.apply_async(song.download, (save_location,))
            
        pool.close()
        pool.join()
        
        print(f"Finished downloading {self.title}")