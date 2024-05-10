class MusicVideo:
    __artist = ""
    __title = ""
    __url = ""
    __release_year = 0
    __note = ""
    __map = {}

    def __init__(self, artist, title, url, year, note, save=False):
        self.__artist = artist
        self.__title = title
        self.__url = url
        self.__year = year
        self.__note = note
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()


    @classmethod
    def build(cls, video_dict):
        from logic.PerformanceVideo import PerformanceVideo

        if video_dict["type"] == "MusicVideo":
            return MusicVideo(
                video_dict["artist"],
                video_dict["title"],
                video_dict["url"],
                video_dict["year"],
                video_dict["note"]
            )
        elif video_dict["type"] == "PerformanceVideo":
            return PerformanceVideo(
                video_dict["artist"],
                video_dict["title"],
                video_dict["url"],
                video_dict["year"],
                video_dict["note"],
                video_dict["location"],
                video_dict["performance_date"]
            )

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "type": "MusicVideo",
            "artist": self.__artist,
            "title": self.__title,
            "url": self.__url,
            "year": self.__year,
            "note": self.__note
        }

    def get_key(self):
        return f"{self.__artist}: {self.__title}".lower()

    @staticmethod
    def make_key(artist, title):
        return f"{artist}: {title}".lower()

    def get_artist(self):
        return self.__artist

    def get_title(self):
        return self.__title

    def update_note(self, note):
        self.__note = note
        self.save()

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def delete(self):
        from data.Database import Database

        del self.__class__.__map[self.get_key()]
        Database.delete_playlist(self)

    def __str__(self):
        return f"{self.__title} by {self.__artist}: {self.__url}. {self.__note}."

    def to_html(self):
        return f"<a href='{self.__url}'>{self.__title}</a>, {self.__artist} - {self.__note}."

    @staticmethod
    def get_videos():
        from data.Database import Database

        return Database.get_videos()

    def save(self):
        from data.Database import Database

        Database.save_video(self)
