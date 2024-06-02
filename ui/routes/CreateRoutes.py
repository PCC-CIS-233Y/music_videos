from ui.WebUI import WebUI
from flask import render_template, request
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo

class CreateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_playlist')
    def create_playlist():
        return render_template("create/create_playlist.html")

    @staticmethod
    @__app.route('/do_create_playlist', methods=['GET', 'POST'])
    def do_create_playlist():
        name, error = WebUI.validate_field("The playlist name", "name")
        if name is None:
            return error
        key = name.lower()
        playlist = WebUI.lookup_playlist(key)
        if playlist is not None:
            return render_template(
                "error.html",
                message_header="Playlist already exists!",
                message_body=f"A playlist named {name} already exists. Please choose another name and try again."
            )
        if "thumbnail" in request.form:
            thumbnail = request.form["thumbnail"].strip()
        else:
            thumbnail = ""
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""
        playlist = PlayList(
            name, [], thumbnail, description, WebUI.get_user_key(), WebUI.get_playlist_map(), save=True
        )
        WebUI.get_all_playlists().append(playlist)
        return render_template("create/confirm_playlist_created.html", playlist=playlist)

    @staticmethod
    @__app.route('/create_music_video')
    def create_music_video():
        return render_template("create/create_music_video.html")

    @staticmethod
    @__app.route('/do_create_music_video', methods=['GET', 'POST'])
    def do_create_music_video():
        # artist title url year note
        artist, error = WebUI.validate_field("The music video artist", "artist")
        if artist is None:
            return error
        title, error = WebUI.validate_field("The music video title", "title")
        if title is None:
            return error
        key = MusicVideo.make_key(artist, title).lower()
        video = WebUI.lookup_video(key)
        if video is not None:
            return render_template(
                "error.html",
                message_header=f"A music Video already exists!",
                message_body=f"A music video with the title '{title}' by '{artist}' already exists. Please choose another video and try again."
            )
        url, error = WebUI.validate_field("The music video URL", "url")
        if url is None:
            return error
        if "year" in request.form:
            year = request.form["year"].strip()
        else:
            year = ""
        if "note" in request.form:
            note = request.form["note"].strip()
        else:
            note = ""
        video = MusicVideo(artist, title, url, year, note, WebUI.get_user_key(), WebUI.get_video_map(), save=True)
        WebUI.get_all_videos().append(video)
        return render_template("create/confirm_music_video_created.html", video=video)

    @staticmethod
    @__app.route('/create_performance_video')
    def create_performance_video():
        return render_template("create/create_performance_video.html")

    @staticmethod
    @__app.route('/do_create_performance_video', methods=['GET', 'POST'])
    def do_create_performance_video():
        # artist title url year note
        artist, error = WebUI.validate_field("The performance video artist", "artist")
        if artist is None:
            return error
        title, error = WebUI.validate_field("The performance video title", "title")
        if title is None:
            return error
        location, error = WebUI.validate_field("The performance video location", "location")
        if location is None:
            return error
        performance_date, error = WebUI.validate_field("The performance date of the performance video", "performance_date")
        if performance_date is None:
            return error
        key = PerformanceVideo.make_key(artist, title, location, performance_date).lower()
        video = WebUI.lookup_video(key)
        if video is not None:
            return render_template(
                "error.html",
                message_header=f"A performance video already exists!",
                message_body=f"A performance video with the title '{title}' by '{artist}' in {location} on {performance_date} already exists. Please choose another video and try again."
            )
        url, error = WebUI.validate_field("The performance video URL", "url")
        if url is None:
            return error
        if "year" in request.form:
            year = request.form["year"].strip()
        else:
            year = ""
        if "note" in request.form:
            note = request.form["note"].strip()
        else:
            note = ""
        video = PerformanceVideo(
            artist, title, url, year, note, WebUI.get_user_key(), WebUI.get_video_map(),
            location, performance_date, save=True
        )
        WebUI.get_all_videos().append(video)
        return render_template("create/confirm_performance_video_created.html", video=video)

    @staticmethod
    @__app.route("/join_playlists")
    def join_playlists():
        return render_template("create/join_playlists.html", playlists=WebUI.get_all_playlists())

    @staticmethod
    @__app.route("/do_join_playlists", methods=["GET", "POST"])
    def do_join_playlists():
        first_key, error = WebUI.validate_field("The first playlist name", "first_playlist")
        if first_key is None:
            return error
        second_key, error = WebUI.validate_field("The second playlist name", "second_playlist")
        if second_key is None:
            return error
        first_playlist = WebUI.lookup_playlist(first_key.lower())
        if first_playlist is None:
            return render_template(
                "error.html",
                message_header=f"The playlist {first_key} was not found.",
                message_body=f"A playlist with the name '{first_key}' was not found. Please choose another playlist and try again."
            )
        second_playlist = WebUI.lookup_playlist(second_key.lower())
        if second_playlist is None:
            return render_template(
                "error.html",
                message_header=f"The playlist {second_key} was not found.",
                message_body=f"A playlist with the name '{second_key}' was not found. Please choose another playlist and try again."
            )
        new_key = f"{first_playlist.get_name()}/{second_playlist.get_name()}"
        new_playlist = WebUI.lookup_playlist(new_key.lower())
        if new_playlist is not None:
            return render_template(
                "error.html",
                message_header=f"The playlist {new_key} already exists.",
                message_body=f"A playlist with the name '{new_key}' already exists. Please choose another playlist and try again."
            )
        new_playlist = first_playlist + second_playlist
        WebUI.get_all_playlists().append(new_playlist)
        return render_template(
            "create/confirm_playlists_joined.html",
            first_playlist=first_playlist,
            second_playlist=second_playlist,
            new_playlist=new_playlist
        )