from song import Song
import os
from multiprocessing import Pool


class Playlist:
    __slots__ = ("id", "title", "songs")

    def __init__(self, id: str, title: str, songs: list):
        self.id = id
        self.title = title
        self.songs = songs

    def __str__(self):
        return f"{self.title} with {len(self.songs)} songs"

    @staticmethod
    def get_playlist(user, id: str, limit: int = None):
        try:
            data = user.api.get_playlist(id, limit=limit)
        except Exception as e:
            print(f"Error getting playlist {id}. Some playlist types are not supported yet.")
            return None
            
        title = data["title"]
        songs = []
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

        return Playlist(id, title, songs)
    
    @staticmethod
    def get_watch_playlist(user, videoId: str, playlistId: str, limit: int = None):
        data = user.api.get_watch_playlist(videoId, playlistId)
        title = data["tracks"][0]["title"]
        songs = []
        
        for song in data["tracks"]:
            if song["videoId"] is not None:
                songs.append(
                    Song(
                        id=song["videoId"],
                        title=song["title"],
                        artist=", ".join([artist["name"]
                                        for artist in song["artists"]]),
                        # convert m:s to seconds
                        time=song["length"].split(":")[0] * 60 + song["length"].split(":")[1],
                        thumbnails=song["thumbnail"],
                    )
                )
            else:
                print(f"Skipping {song['title']} because it is unavailable")
                
            if limit is not None and len(songs) >= limit:
                break
                
        return Playlist(playlistId, title, songs)
    
    @staticmethod
    def get_playlist_from_album(user, albumId: str, limit: int = None):
        data = user.api.get_album(albumId)
        title = data["title"]
        songs = []
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
                
            if limit is not None and len(songs) >= limit:
                break
                
        return Playlist(albumId, title, songs)
    
    @staticmethod
    def get_playlist_from_artist(user, artistId: str, limit: int = None):
        artist = user.api.get_artist(artistId)
            
        return Playlist.get_playlist(user, artist["songs"]["browseId"], limit=limit)
    
    @staticmethod
    def get_playlist_from_likes(user, limit: int = None):
        return Playlist.get_playlist(user, user.api.get_liked_songs(limit=limit))
    
    def download(self, save_location: str, save_to_subfolder: bool = True, processes: int = 12, format: str = "mp3"):
        print(f"Downloading {self.title} with {len(self.songs)} songs")
        
        if not os.path.exists(save_location):
            os.mkdir(save_location)
        
        if save_to_subfolder:
            
            # Make directory
            save_location = f"{save_location}/{self.title}"
            
            if not os.path.exists(save_location):
                os.mkdir(save_location)

        pool = Pool(processes=processes)
        
        for song in self.songs:
            pool.apply_async(song.download, (save_location,format,))

        pool.close()
        pool.join()
        
        print(f"Finished downloading {self.title}")
