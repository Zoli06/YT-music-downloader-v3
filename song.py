import contextlib
import io
import yt_dlp as youtube_dl
import sys


class Song:
    __slots__ = ("id", "title", "artist", "album", "time", "genre", "thumbnails")

    # constructor
    def __init__(
        self,
        id: str,
        title: str,
        artist: str = "Unknown artist",
        album: str = None,
        time: int = None,
        genre: str = None,
        thumbnails: list = None,
    ):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.genre = genre
        self.thumbnails = thumbnails

    def __str__(self):
        return f"{self.title} by {self.artist}, {self.time} seconds long"

    # get song from youtube music api
    @staticmethod
    def get_song(user, id: str):
        data = user.api.get_song(id)
        data = data["videoDetails"]
        title = data["title"]
        artist = data["author"]
        time = data["lengthSeconds"]
        thumbnails = data["thumbnail"]["thumbnails"]
        return Song(id, title, artist, time=time, thumbnails=thumbnails)

    def download(self, save_location: str, format: str = "mp3"):
        # download song
        try:           
            # Download quietly with youtube_dl
            ydl_opts = {
                "quiet": True,
                "format": "bestaudio/best",
                "outtmpl": f"{save_location}/{self.artist.replace('/', '_')} - {self.title.replace('/', '_')}.%(ext)s",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": format,
                        "preferredquality": "192",
                    },
                    {"key": "EmbedThumbnail"},
                    {"key": "FFmpegMetadata"},
                ],
                "addmetadata": True,
            }
            
            # In some cases, youtube_dl will refuse to shut up
            with contextlib.redirect_stdout(io.StringIO()):
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={self.id}"])
        except Exception as e:
            print(f"Error downloading {self.title} by {self.artist}: {e}\n")
