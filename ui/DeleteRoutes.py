from ui.WebUI import WebUI
from flask import render_template, request
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo


class DeleteRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/delete_playlist")
    def delete_playlist():
        return render_template("delete/delete_playlist.html", playlists=WebUI.get_all_playlists())

    @staticmethod
    @__app.route("/do_delete_playlist", methods=["GET", "POST"])
    def do_delete_playlist():
        playlist_key, error = WebUI.validate_field("The playlist name", "playlist")
        if playlist_key is None:
            return error
        playlist = PlayList.lookup(playlist_key.lower())
        if playlist is None:
            return render_template(
                "error.html",
                message_header=f"The playlist {playlist_key} was not found.",
                message_body=f"A playlist with the name '{playlist_key}' was not found. Please choose another playlist and try again."
            )
        if playlist.get_name() == PlayList.ALL_VIDEOS:
            return render_template(
                "error.html",
                message_header=f"Cannot delete playlist.",
                message_body=f"You cannot the '{PlayList.ALL_VIDEOS}' playlist."
            )
        WebUI.get_all_playlists().remove(playlist)
        playlist.delete()
        return render_template("delete/confirm_playlist_deleted.html", playlist=playlist)

    @staticmethod
    @__app.route("/delete_video")
    def delete_video():
        return render_template("delete/delete_video.html", videos=WebUI.get_all_videos())

    @staticmethod
    @__app.route("/do_delete_video", methods=["GET", "POST"])
    def do_delete_video():
        video_key, error = WebUI.validate_field("The video", "video")
        if video_key is None:
            return error
        video = MusicVideo.lookup(video_key)
        if video is None:
            return render_template(
                "error.html",
                message_header="Video does not exist!",
                message_body=f"The video {video_key} does not exist. Please choose another video and try again."
            )
        for playlist in WebUI.get_all_playlists():
            if video in playlist:
                playlist.remove(video)
        video.delete()
        return render_template("delete/confirm_video_deleted.html", video=video)
