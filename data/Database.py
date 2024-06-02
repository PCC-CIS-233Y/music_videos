from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo
from logic.PlayList import PlayList
from logic.User import User
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configparser import ConfigParser
import os
import bcrypt


class Database:
    __connection = None
    __database = None
    __videos_collection = None
    __playlists_collection = None
    __users_collection = None
    APP_NAME = "music_box"

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            if "APPDATA" in os.environ:
                path = f"{os.environ['APPDATA']}\\{cls.APP_NAME}\\{cls.APP_NAME}.ini"
            elif "HOME" in os.environ:
                path = f"{os.environ['HOME']}/{cls.APP_NAME}/{cls.APP_NAME}.ini"
            else:
                raise Exception("Couldn't find config directory.")

            config_parser = ConfigParser()
            config_parser.read(path)
            username = config_parser["Database"]["username"]
            password = config_parser["Database"]["password"]
            cluster = config_parser["Database"]["cluster"]

            uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.MusicBox
            cls.__videos_collection = cls.__database.Videos
            cls.__playlists_collection = cls.__database.PlayLists
            cls.__users_collection = cls.__database.Users

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
        cls.__users_collection.drop()
        cls.__users_collection = cls.__database.Users


        all_videos, all_playlists, all_users = cls.get_playlists()

        user_dicts = [user.to_dict() for user in all_users]
        cls.__users_collection.insert_many(user_dicts)

        video_dicts = [video.to_dict() for video in all_videos]
        cls.__videos_collection.insert_many(video_dicts)

        playlist_dicts = [playlist.to_dict() for playlist in all_playlists]
        cls.__playlists_collection.insert_many(playlist_dicts)

    @classmethod
    def read_data(cls, user_key):
        cls.connect()
        video_map = {}
        video_dicts = list(cls.__videos_collection.find({"user_key": user_key}))
        videos = [MusicVideo.build(video_dict, video_map) for video_dict in video_dicts]

        playlist_map = {}
        playlist_dicts = list(cls.__playlists_collection.find({"user_key": user_key}))
        playlists = [PlayList.build(playlist_dict, playlist_map, video_map) for playlist_dict in playlist_dicts]

        return playlist_map[PlayList.make_key(PlayList.ALL_VIDEOS)], playlists, video_map, playlist_map

    @classmethod
    def read_user(cls, username):
        cls.connect()
        user_dict = cls.__users_collection.find_one({'_id': username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def get_playlists(cls):
        user1 = User("Marc", b'$2b$13$On/tiWsXnQd7ZbZ9z3e8VudUksO3byC4aTApfG9a7SA48t5UuIVMC')
        user2 = User("Mighty Mouse", b'$2b$13$EryH8O6HXIkopYOj2XwKbOoOphXORLu9SoxGWkCFLxw2w/OqkJDAC')

        video_map = {}
        playlist_map = {}

        bs_bbl = MusicVideo(
            "Bruce Springsteen",
            "Blinded by the Light",
            "https://www.youtube.com/watch?v=xPy82OO6vRg",
            1973,
            "The original version",
            user1.get_key(),
            video_map
        )
        mm_bbl = MusicVideo(
            "Manfred Mann's Earth Band",
            "Blinded by the Light",
            "https://www.youtube.com/watch?v=Rzk3x3HZbJI",
            1976,
            "Cover version of a song by Bruce Springsteen",
            user1.get_key(),
            video_map
        )
        bs_btn = PerformanceVideo(
            "Bruce Springsteen",
            "Because the Night",
            "https://www.youtube.com/watch?v=-Evp0MrJ9lk",
            1978,
            "Written by Bruce and Patti Smith",
            user1.get_key(),
            video_map,
            "Houston",
            "1978")
        ps_btn = MusicVideo(
            "Patti Smith",
            "Because the Night",
            "https://www.youtube.com/watch?v=c_BcivBprM0",
            1978,
            "Written by Bruce and Patti",
            user1.get_key(),
            video_map
        )
        kb_ruth = MusicVideo(
            "Kate Bush",
            "Running up that Hill",
            "https://www.youtube.com/watch?v=wp43OdtAAkM&ab_channel=KateBushMusic",
            1985,
            "Song surged in popularity due to its use in Stranger Things",
            user1.get_key(),
            video_map
        )
        kbpg_dgu = MusicVideo(
            "Kate Bush and Peter Gabriel",
            "Don't Give Up",
            "https://www.youtube.com/watch?v=VjEq-r2agqc&ab_channel=PeterGabriel",
            1986,
            "Video was very popular on MTV for a long time",
            user1.get_key(),
            video_map
        )
        pg_sh = PerformanceVideo(
            "Peter Gabriel",
            "Solsbury Hill",
            "https://www.youtube.com/watch?v=WeYqJxlSv-Y&ab_channel=PeterGabriel",
            1977,
            "Montage of live performances spanning 35 years",
            user1.get_key(),
            video_map,
            "Various locations",
            "1978-2013"
        )
        ec_a = MusicVideo(
            "Elvis Costello",
            "Alison",
            "https://www.youtube.com/watch?v=C9GlC9GyF4Y",
            "Almost 50 years old",
            "1977",
            user2.get_key(),
            video_map
        )
        ec_rr = PerformanceVideo(
            "Elvis Costello",
            "Radio Radio",
            "https://www.youtube.com/watch?v=eD_24nDzkeo",
            "1977",
            "First time I saw Elvis Costello",
            user2.get_key(),
            video_map,
            "Saturday Night Live",
            "December 17th, 1977"
        )

        bs = PlayList(
            "Bruce Springsteen",
            [bs_bbl, bs_btn],
            "https://glassgirder.com/music_player/images/bruce.jpg",
            "The singer/composer Bruce Springsteen",
            user1.get_key(),
            playlist_map
        )
        ps = PlayList(
            "Patti Smith",
            [ps_btn],
            "https://glassgirder.com/music_player/images/patti.jpg",
            "Patti Smith",
            user1.get_key(),
            playlist_map
        )
        pg = PlayList(
            "Peter Gabriel",
            [pg_sh, kbpg_dgu],
            "https://scontent.fhio2-2.fna.fbcdn.net/v/t1.6435-9/118160015_10158314269559760_6423978243084146145_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=5f2048&_nc_ohc=Qn6PPdcyNjMAb4f8ycC&_nc_ht=scontent.fhio2-2.fna&oh=00_AfDHmwc7zpKQomT3vtcycXL3xCXB-Sc4n9UhbeL5mvQ_2A&oe=66552280",
            "Formerly drummer for Genesis",
            user1.get_key(),
            playlist_map
        )
        kb = PlayList(
            "Kate Bush",
            [kbpg_dgu, kb_ruth],
            "https://i.iheart.com/v3/surl/aHR0cDovL2ltYWdlLmloZWFydC5jb20vaW1hZ2VzL292ZXJyaWRlLzM3OTM2XzZlMzA0ZTBiLTkyMDUtNGI5My04YWU3LTczYWFhMGYyOWNiMi5qcGc=?ops=fit%28480%2C480%29%2Crun%28%22circle%22%29&sn=eGtleWJhc2UyMDIxMTExMDo6_8saG4AYSLrIWkuwdc_DolZpM7mBlOcsM5ALSb_88w%3D%3D&surrogate=1cOXl179JY-syhxYSCX6Q1a_Mcu6UO8d-F4oJzpZf1hcUbJr4aImw9gKF1etygNPvEf1drJMM41pDkyR0A231uXuml9Gz_YQA80xUi4rA7aMuVDGzKutY5QxBOSe18ws_xl8GBXkEEGxV0VwwaYHO7Z1bXq_rK2ysgUqcKI6YkDJq3dJeVT0mXQ3VuQBvjB_9u1dxeOlL5YsvsMp59C5RAMY1MPtumR0Ljm78eHVmW_LFPSU2VmfNuyt9VupNihj",
            "Discovered by David Gilmore of Pink Floyd",
            user1.get_key(),
            playlist_map
        )
        ec = PlayList(
            "Elvis Costello",
            [ec_a, ec_rr],
            "https://media.wired.com/photos/5a14c30e12f1404a56f1b7d0/master/w_2240,c_limit/elviscostello.jpg",
            "Declan Patrick MacManus, OBE",
            user2.get_key(),
            playlist_map
        )

        u1_all = PlayList(
            PlayList.ALL_VIDEOS,
            [bs_bbl, mm_bbl, bs_btn, ps_btn, pg_sh, kbpg_dgu, kb_ruth],
            "https://glassgirder.com/music_player/images/all_videos.jpg",
            "All Videos for Marc",
            user1.get_key(),
            playlist_map
        )
        u2_all = PlayList(
            PlayList.ALL_VIDEOS,
            [ec_a, ec_rr],
            "https://glassgirder.com/music_player/images/all_videos.jpg",
            "All Videos for Mighty Mouse",
            user2.get_key(),
            playlist_map
        )

        return [bs_bbl, mm_bbl, bs_btn, ps_btn, pg_sh, kbpg_dgu, kb_ruth, ec_a, ec_rr], [bs, ps, pg, kb, ec, u1_all, u2_all], [user1, user2]

    @classmethod
    def save_playlist(cls, playlist):
        cls.connect()
        playlist_dict = playlist.to_dict()
        cls.__playlists_collection.update_one({"_id": playlist_dict["_id"]}, {"$set": playlist_dict}, upsert=True)

    @classmethod
    def save_video(cls, video):
        cls.connect()
        video_dict = video.to_dict()
        cls.__videos_collection.update_one({"_id": video_dict["_id"]}, {"$set": video_dict}, upsert=True)

    @classmethod
    def add_user(cls, user):
        cls.connect()
        user_dict = user.to_dict()
        cls.__users_collection.insert_one(user_dict)

    @classmethod
    def delete_playlist(cls, playlist):
        cls.connect()
        cls.__playlists_collection.delete_one({"_id": playlist.get_id()})

    @classmethod
    def delete_video(cls, video):
        cls.connect()
        cls.__videos_collection.delete_one({"_id": video.get_id()})


if __name__ == "__main__":
    Database.connect()
    print(Database.read_user("John"))
