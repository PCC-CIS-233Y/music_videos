from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo
from logic.PlayList import PlayList
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Database:
    PASSWORD = 'RXZaZJRhmSsnWZcq'
    USERNAME = 'PlayListManager'
    CLUSTER = 'cluster0.kfwjfnl.mongodb.net'
    __connection = None
    __database = None
    __videos_collection = None
    __playlists_collection = None
    URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            cls.__connection = MongoClient(cls.URI, server_api=ServerApi('1'))
            cls.__database = cls.__connection.MusicBox
            cls.__videos_collection = cls.__database.Videos
            cls.__playlists_collection = cls.__database.PlayLists

            # print("Client:", cls.__connection)
            # print("Database:", cls.__database)
            # print("Videos:", cls.__videos_collection)
            # print("Playlists:", cls.__playlists_collection)

    @classmethod
    def rebuild_data(cls):
        cls.connect()

        # Remake both collections
        cls.__videos_collection.drop()
        cls.__videos_collection = cls.__database.Videos
        cls.__playlists_collection.drop()
        cls.__playlists_collection = cls.__database.PlayLists

        all_videos, all_playlists = cls.get_playlists()

        video_dicts = [video.to_dict() for video in all_videos]
        cls.__videos_collection.insert_many(video_dicts)

        playlist_dicts = [playlist.to_dict() for playlist in all_playlists]
        cls.__playlists_collection.insert_many(playlist_dicts)

    @classmethod
    def read_data(cls):
        cls.connect()
        video_dicts = list(cls.__videos_collection.find())
        videos = [MusicVideo.build(video_dict) for video_dict in video_dicts]

        playlist_dicts = list(cls.__playlists_collection.find())
        playlists = [PlayList.build(playlist_dict) for playlist_dict in playlist_dicts]

        return PlayList.lookup(PlayList.ALL_VIDEOS), playlists

    @classmethod
    def get_playlists(cls):
        bs_bbl = MusicVideo("Bruce Springsteen", "Blinded by the Light",
                            "https://www.youtube.com/watch?v=xPy82OO6vRg", 1973, "The original version")
        mm_bbl = MusicVideo("Manfred Mann's Earth Band", "Blinded by the Light",
                            "https://www.youtube.com/watch?v=Rzk3x3HZbJI", 1976,
                            "Cover version of a song by Bruce Springsteen")
        bs_btn = PerformanceVideo("Bruce Springsteen", "Because the Night",
                                  "https://www.youtube.com/watch?v=-Evp0MrJ9lk", 1978,
                                  "Written by Bruce and Patti Smith", "Houston", "1978")
        ps_btn = MusicVideo("Patti Smith", "Because the Night",
                            "https://www.youtube.com/watch?v=c_BcivBprM0", 1978,
                            "Written by Bruce and Patti")
        kb_ruth = MusicVideo("Kate Bush", "Running up that Hill",
                             "https://www.youtube.com/watch?v=wp43OdtAAkM&ab_channel=KateBushMusic", 1985,
                             "Song surged in popularity due to its use in Stranger Things.")
        kbpg_dgu = MusicVideo("Kate Bush and Peter Gabriel", "Don't Give Up",
                              "https://www.youtube.com/watch?v=VjEq-r2agqc&ab_channel=PeterGabriel", 1986,
                              "Video was very popular on MTV for a long time.")
        pg_sh = PerformanceVideo("Peter Gabriel", "Solsbury Hill",
                                 "https://www.youtube.com/watch?v=WeYqJxlSv-Y&ab_channel=PeterGabriel", 1977,
                                 "Montage of live performances spanning 35 years.",
                                 "Various locations", "1978-2013")

        bs = PlayList("Bruce Springsteen", [bs_bbl, bs_btn],
                      "https://glassgirder.com/music_player/images/bruce.jpg",
                      "The singer/composer Bruce Springsteen")
        ps = PlayList("Patti Smith", [ps_btn],
                      "https://glassgirder.com/music_player/images/patti.jpg",
                      "Patti Smith")
        pg = PlayList("Peter Gabriel", [pg_sh, kbpg_dgu],
                      "https://scontent.fhio2-2.fna.fbcdn.net/v/t1.6435-9/118160015_10158314269559760_6423978243084146145_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=5f2048&_nc_ohc=Qn6PPdcyNjMAb4f8ycC&_nc_ht=scontent.fhio2-2.fna&oh=00_AfDHmwc7zpKQomT3vtcycXL3xCXB-Sc4n9UhbeL5mvQ_2A&oe=66552280",
                      "Formerly drummer for Genesis.")
        kb = PlayList("Kate Bush", [kbpg_dgu, kb_ruth],
                      "https://i.iheart.com/v3/surl/aHR0cDovL2ltYWdlLmloZWFydC5jb20vaW1hZ2VzL292ZXJyaWRlLzM3OTM2XzZlMzA0ZTBiLTkyMDUtNGI5My04YWU3LTczYWFhMGYyOWNiMi5qcGc=?ops=fit%28480%2C480%29%2Crun%28%22circle%22%29&sn=eGtleWJhc2UyMDIxMTExMDo6_8saG4AYSLrIWkuwdc_DolZpM7mBlOcsM5ALSb_88w%3D%3D&surrogate=1cOXl179JY-syhxYSCX6Q1a_Mcu6UO8d-F4oJzpZf1hcUbJr4aImw9gKF1etygNPvEf1drJMM41pDkyR0A231uXuml9Gz_YQA80xUi4rA7aMuVDGzKutY5QxBOSe18ws_xl8GBXkEEGxV0VwwaYHO7Z1bXq_rK2ysgUqcKI6YkDJq3dJeVT0mXQ3VuQBvjB_9u1dxeOlL5YsvsMp59C5RAMY1MPtumR0Ljm78eHVmW_LFPSU2VmfNuyt9VupNihj",
                      "Discovered by David Gilmore of Pink Floyd.")

        all = PlayList(PlayList.ALL_VIDEOS, [bs_bbl, mm_bbl, bs_btn, ps_btn, pg_sh, kbpg_dgu, kb_ruth],
                       "https://glassgirder.com/music_player/images/all_videos.jpg",
                       "All Videos")

        return all, [bs, ps, pg, kb, all]

    @classmethod
    def save_playlist(cls, playlist):
        cls.connect()
        cls.__playlists_collection.update_one({"_id": playlist.get_key()}, {"$set": playlist.to_dict()}, upsert=True)

    @classmethod
    def save_video(cls, video):
        cls.connect()
        cls.__videos_collection.update_one({"_id": video.get_key()}, {"$set": video.to_dict()}, upsert=True)

    @classmethod
    def delete_playlist(cls, playlist):
        cls.connect()
        cls.__playlists_collection.delete_one({"_id": playlist.get_key()})

    @classmethod
    def delete_video(cls, video):
        cls.connect()
        cls.__videos_collection.delete_one({"_id": video.get_key()})


if __name__ == "__main__":
    Database.connect()
