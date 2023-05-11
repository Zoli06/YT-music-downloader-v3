from library import Library
from user import User
import shutil


def main():
    # I only tested this on Linux
    # But I guess it will work on Windows too
    # UPDATE: Fails with 429
    # Haven't investigated yet
    # Maybe my pc is too fast
    # Sufferring from success

    # IMPORTANT: Don't forget to install ffmpeg command line tool
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found")
        exit(1)

    # Login
    user = User()
    
    # IMPORTANT: get_user_home already includes liked songs for me and likely for you too
    # But if it doesn't for you, you can use get_playlist_from_likes
    # See playlist.py

    lib = Library.get_user_library(user, playlist_limit=None) + Library.get_user_home(
        user,
        include_playlists=True,
        # Special playlist type
        include_watch_playlists=True,
        include_albums=True,
        include_artists=True,
        # Limit how many songs to download from each playlist
        playlist_limit=None,
    )

    # Set save_to_subfolders to False to remove duplicate songs
    # Downside: You won't see which song is from which playlist
    # But most times it's in the mp3 metadata
    lib.download(
        download_location="downloads",
        save_to_subfolders=False,
        processess=6,
        format="mp3",
    )


if __name__ == "__main__":
    main()
