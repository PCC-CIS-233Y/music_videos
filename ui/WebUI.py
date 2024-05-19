from flask import Flask, render_template, request
from logic.PlayList import PlayList


class WebUI:
    __all_videos = None
    __all_playlists = None
    __app = Flask(__name__)
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
    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        from ui.PrintRoutes import PrintRoutes
        from ui.CreateRoutes import CreateRoutes
        from ui.UpdateRoutes import UpdateRoutes
        from ui.DeleteRoutes import DeleteRoutes

        cls.__app.run(host="0.0.0.0", port=8000)
