class MusicVideo:
    __artist = ""
    __title = ""
    __url = ""
    __release_year = 0
    __note = ""
    __user_key = ""

    def __init__(self, artist, title, url, year, note, user_key, video_map, save=False):
        self.__artist = artist
        self.__title = title
        self.__url = url
        self.__year = year
        self.__note = note
        self.__user_key = user_key
        video_map[self.get_key()] = self
        if save:
            self.save()


    @classmethod
    def build(cls, video_dict, video_map):
        from logic.PerformanceVideo import PerformanceVideo

        if video_dict["type"] == "MusicVideo":
            return MusicVideo(
                video_dict["artist"],
                video_dict["title"],
                video_dict["url"],
                video_dict["year"],
                video_dict["note"],
                video_dict["user_key"],
                video_map
            )
        elif video_dict["type"] == "PerformanceVideo":
            return PerformanceVideo(
                video_dict["artist"],
                video_dict["title"],
                video_dict["url"],
                video_dict["year"],
                video_dict["note"],
                video_dict["user_key"],
                video_map,
                video_dict["location"],
                video_dict["performance_date"]
            )

    def to_dict(self):
        return {
            "_id": self.get_id(),
            "type": "MusicVideo",
            "artist": self.__artist,
            "title": self.__title,
            "url": self.__url,
            "year": self.__year,
            "note": self.__note,
            "user_key": self.__user_key
        }

    def get_id(self):
        return f"{self.get_key()}|{self.__user_key}"

    def get_key(self):
        return f"{self.__artist}: {self.__title}".lower()

    def get_printable_key(self):
        return f"{self.__artist}: {self.__title}"

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

    def delete(self):
        from data.Database import Database
        from logic.UserState import UserState

        video_key = self.get_key()
        user_state = UserState.lookup(self.__user_key)
        video_map = user_state.get_video_map()
        if video_key in video_map:
            del video_map[video_key]
        Database.delete_video(self)

    def __str__(self):
        return f"{self.__title} by {self.__artist}: {self.__url}. {self.__note}."

    def to_html(self):
        return f"<a href='{self.__url}'>{self.__title}</a>, {self.__artist} - {self.__note}."

    def save(self):
        from data.Database import Database

        Database.save_video(self)
