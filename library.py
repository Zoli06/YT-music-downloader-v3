from playlist import Playlist


class Library:
    __slots__ = "playlists"

    def __init__(self, playlists: list):
        self.playlists = playlists

    def __str__(self):
        return f"{len(self.playlists)} playlists"

    def __add__(self, other):
        # Add two libraries together and remove duplicates by playlistId
        playlists = self.playlists + other.playlists
        playlists = list({playlist.id: playlist for playlist in playlists}.values())
        return Library(playlists)

    def add_playlist(self, playlist: Playlist):
        self.playlists.append(playlist)

    @staticmethod
    def get_user_library(user, playlist_limit: int = None):
        data = user.api.get_library_playlists()
        playlists = []
        for playlist in data:
            playlist = Playlist.get_playlist(user, playlist["playlistId"], playlist_limit)

            if playlist is not None:
                playlists.append(playlist)

        return Library(playlists)

    @staticmethod
    def get_user_home(
        user,
        include_playlists: bool = True,
        include_watch_playlists: bool = True,
        include_albums: bool = True,
        include_artists: bool = True,
        playlist_limit: int = None,
    ):
        data = user.api.get_home()
        playlists = []

        for row in data:
            for item in row["contents"]:
                if "playlistId" in item and not "videoId" in item:
                    if include_playlists:
                        playlist = Playlist.get_playlist(
                            user, item["playlistId"], playlist_limit
                        )

                        if playlist is not None:
                            playlists.append(playlist)
                elif "playlistId" in item and "videoId" in item:
                    if include_watch_playlists:
                        playlist = Playlist.get_watch_playlist(
                            user, item["videoId"], item["playlistId"], playlist_limit
                        )

                        if playlist is not None:
                            playlists.append(playlist)
                elif "browseId" in item:
                    # If starting with MPREb it is an album
                    # get audioplaylistId from api
                    if item["browseId"].startswith("MPREb"):
                        if include_albums:
                            playlist = Playlist.get_playlist_from_album(
                                user, item["browseId"], playlist_limit
                            )

                            if playlist is not None:
                                playlists.append(playlist)
                    # Check if it is an artist
                    elif item["browseId"].startswith("UC"):
                        if include_artists:
                            playlist = Playlist.get_playlist_from_artist(
                                user, item["browseId"], playlist_limit
                            )

                            if playlist is not None:
                                playlists.append(playlist)
                else:
                    pass

        return Library(playlists)

    def download(
        self,
        save_location: str,
        save_to_subfolders: bool = True,
        processess: int = 12,
        format: str = "mp3",
    ):
        for playlist in self.playlists:
            playlist.download(save_location, save_to_subfolders, processess, format)
