from flask import Flask, render_template, request
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo

class WebUI:
    __all_videos = None
    __all_playlists = None
    __app = Flask(__name__)
    MENU = {
        "Print": {
            "print_playlist?playlist=All%20Videos": "Print a list of all videos.",
            "print_playlists": "Print a list of all playlists."
        },
        "Create": {
            "create_video": "Create a new video.",
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
    def init(cls):
        cls.__all_videos, cls.__all_playlists = PlayList.read_data()

    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @staticmethod
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @__app.route('/print_playlists')
    @staticmethod
    def print_playlists():
        return render_template("print/print_playlists.html", playlists=WebUI.__all_playlists)

    @__app.route('/print_playlist')
    @staticmethod
    def print_playlist():
        if "playlist" not in request.args:
            return render_template(
                "error.html",
                message_header="Playlist not specified!",
                message_body="No playlist was specified. Please check the URL and try again."
            )
        key = request.args["playlist"]
        playlist = PlayList.lookup(key)
        if playlist is None:
            return render_template(
                "error.html",
                message_header="Playlist not found!",
                message_body=f"The Playlist named '{key}' was not found. Please check the URL and try again."
            )
        return render_template("print/print_playlist.html", playlist=playlist)

    @classmethod
    def run(cls):
        cls.__app.run(port=8000)


if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
