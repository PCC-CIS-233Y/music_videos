from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from logic.PlayList import PlayList
import os
import bcrypt


class WebUI:
    __all_videos = None
    __all_playlists = None
    __app = Flask(__name__)
    ALLOWED_PATHS = [
        "/login",
        "/do_login",
        "/static/music_box.css"
    ]
    MENU = {
        "Print": {
            "print_playlist?playlist=All%20Videos": "Print a list of all videos.",
            "print_playlists": "Print a list of all playlists.",
            "show_playlist_contents": "Select a playlist and show the contents."
        },
        "Create": {
            "create_music_video": "Create a new music video.",
            "create_performance_video": "Create a new performance video.",
            "create_playlist": "Create a new playlist.",
            "join_playlists": "Join two playlists together."
        },
        "Update": {
            "update_video_note": "Update the note for a video.",
            "add_video_to_playlist": "Add a video to a playlist.",
            "remove_video_from_playlist": "Remove a video from a playlist.",
        },
        "Delete": {
            "delete_video": "Delete a video.",
            "delete_playlist": "Delete a playlist."
        }
    }

    @classmethod
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_all_playlists(cls):
        return cls.__all_playlists

    @classmethod
    def get_all_videos(cls):
        return cls.__all_videos

    @classmethod
    def init(cls):
        cls.__all_videos, cls.__all_playlists = PlayList.read_data()

    @classmethod
    def validate_field(cls, object_name, field_name):
        if field_name not in request.form:
            return None, render_template(
                "error.html",
                message_header=f"{object_name} was not specified!",
                message_body=f"{object_name} was not specified. Please check the form and try again."
            )
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template(
                "error.html",
                message_header=f"{object_name} was not specified!",
                message_body=f"{object_name} was not specified. Please check the form and try again."
            )
        return field_value, None

    @staticmethod
    @__app.before_request
    def before_request():
        if "user" not in session:
            if request.path not in WebUI.ALLOWED_PATHS:
                return redirect(url_for("login"))

    @staticmethod
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @__app.route('/')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        from ui.PrintRoutes import PrintRoutes
        from ui.CreateRoutes import CreateRoutes
        from ui.UpdateRoutes import UpdateRoutes
        from ui.DeleteRoutes import DeleteRoutes
        from ui.UserRoutes import UserRoutes

        if "APPDATA" in os.environ:
            path = os.environ["APPDATA"]
        elif "HOME" in os.environ:
            path = os.environ["HOME"]
        else:
            raise Exception("Couldn't find config folder.")

        cls.__app.secret_key = bcrypt.gensalt()
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        Session(cls.__app)

        cls.__app.run(host="0.0.0.0", port=8443, ssl_context=(path + "/music_box/cert.pem", path + "/music_box/key.pem"))

