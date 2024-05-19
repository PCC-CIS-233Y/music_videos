class PlayList:
    ALL_VIDEOS = "All Videos"
    __name = ""
    __videos = []
    __thumbnail = ""
    __description = ""
    __map = {}

    def __init__(self, name, videos, thumbnail, description, save=False):
        self.__name = name
        self.__videos = videos
        self.__thumbnail = thumbnail
        self.__description = description
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, playlist_dict):
        from logic.MusicVideo import MusicVideo

        return PlayList(
            playlist_dict["name"],
            [MusicVideo.lookup(key) for key in playlist_dict["videos"]],
            playlist_dict["thumbnail"],
            playlist_dict["description"]
        )

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "name": self.__name,
            "thumbnail": self.__thumbnail,
            "description": self.__description,
            "videos": [video.get_key() for video in self.__videos]
        }

    def get_key(self):
        return self.__name.lower()

    def get_printable_key(self):
        return self.__name

    def get_name(self):
        return self.__name

    def get_thumbnail(self):
        return self.__thumbnail

    def get_description(self):
        return self.__description

    def __str__(self):
        s = f"""Playlist: {self.__name}
Thumbnail: {self.__thumbnail}, 
Description: {self.__description}, 
Videos: 
"""
        for video in self.__videos:
            s += "    " + str(video) + "\n"
        return s

    @classmethod
    def lookup(cls, key):
        lower_key = key.lower()
        if lower_key in cls.__map:
            return cls.__map[lower_key]
        else:
            return None

    def append(self, video, save=True):
        from data.Database import Database

        self.__videos.append(video)
        if save:
            Database.save_playlist(self)

    def remove(self, video):
        from data.Database import Database
        self.__videos.remove(video)

        Database.save_playlist(self)

    def delete(self):
        from data.Database import Database

        del self.__class__.__map[self.get_key()]
        Database.delete_playlist(self)

    def __iter__(self):
        return self.__videos.__iter__()

    def __contains__(self, video):
        return video in self.__videos

    def __add__(self, other):
        name = f"{self.get_name()}/{other.get_name()}"
        thumbnail = self.get_thumbnail()
        description = self.get_description() + " " + other.get_description()
        new_playlist = PlayList(name, [], thumbnail, description)
        for video in self:
            if video not in new_playlist:
                new_playlist.append(video, save=False)
        for video in other:
            if video not in new_playlist:
                new_playlist.append(video, save=False)
        new_playlist.save()
        return new_playlist

    @staticmethod
    def get_playlists():
        from data.Database import Database

        return Database.get_playlists()

    @staticmethod
    def rebuild_data():
        from data.Database import Database

        return Database.rebuild_data()

    @staticmethod
    def read_data():
        from data.Database import Database

        return Database.read_data()

    def save(self):
        from data.Database import Database

        Database.save_playlist(self)