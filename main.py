from library import Library
from user import User
import shutil

# I only tested this on Linux
# But I guess it will work on Windows too

# IMPORTANT: Don't forget to install ffmpeg command line tool
if not shutil.which('ffmpeg'):
    print('ffmpeg not found')
    exit(1)

# Login
user = User()

# Go see library.py and playlist.py class methods for more options
# I will document them later
# get_user_home already includes liked songs for me
# But if it doesn't for you, you can use get_playlist_from_likes
# See playlist.py
# These commands are customizible
# See library.py
lib = Library.get_user_library(user) + Library.get_user_home(user)

# Set save_to_subfolders to False to remove duplicate songs
# Downside: You won't see which song is from which playlist
# But most times it's in the mp3 metadata
lib.download('downloads', save_to_subfolders=False, processess=12, format='mp3')