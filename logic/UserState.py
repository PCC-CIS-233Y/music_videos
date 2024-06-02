class UserState:
    __user = None
    __all_videos = None
    __all_playlists = None
    __video_map = None
    __playlist_map = None
    __map = {}

    def __init__(self, user):
        from data.Database import Database

        self.__user = user
        self.__all_videos, self.__all_playlists, self.__video_map, self.__playlist_map = Database.read_data(
            user.get_key()
        )
        self.__class__.__map[self.get_key()] = self

    @classmethod
    def logout(cls, user_key):
        if user_key in cls.__map:
            del cls.__map[user_key]

    def get_key(self):
        return self.__user.get_key()

    def get_all_playlists(self):
        return self.__all_playlists

    def get_all_videos(self):
        return self.__all_videos

    def get_playlist_map(self):
        return self.__playlist_map

    def get_video_map(self):
        return self.__video_map

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def lookup_playlist(self, key):
        if key in self.__playlist_map:
            return self.__playlist_map[key]
        return None

    def lookup_video(self, key):
        if key in self.__video_map:
            return self.__video_map[key]
        return None
