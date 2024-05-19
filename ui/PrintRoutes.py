from ui.WebUI import WebUI
from flask import render_template, request
from logic.PlayList import PlayList


class PrintRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/print_playlists')
    def print_playlists():
        return render_template("print/print_playlists.html", playlists=WebUI.get_all_playlists())

    @staticmethod
    @__app.route('/print_playlist')
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

    @staticmethod
    @__app.route('/show_playlist_contents')
    def show_playlist_contents():
        return render_template(
            "print/show_playlist_contents.html",
            playlists=WebUI.get_all_playlists()
        )