from logic.MusicVideo import MusicVideo


class PerformanceVideo(MusicVideo):
    __location = ""
    __performance_date = ""

    def __init__(self, artist, title, url, year, note, location, performance_date, save=False):
        self.__location = location
        self.__performance_date = performance_date
        super().__init__(artist, title, url, year, note, save=save)

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "PerformanceVideo"
        dict["location"] = self.__location
        dict["performance_date"] = self.__performance_date
        return dict

    def get_key(self):
        return f"{self.get_artist()}: {self.get_title()} at {self.__location} on {self.__performance_date}".lower()

    @staticmethod
    def make_key(artist, title, location, performance_date):
        return f"{artist}: {title} at {location} on {performance_date}".lower()

    def __str__(self):
        s = super().__str__()
        return s + f" in {self.__location}, date: {self.__performance_date}"

    def to_html(self):
        html = super().to_html()
        return html + f" A performance in {self.__location}, date: {self.__performance_date}"