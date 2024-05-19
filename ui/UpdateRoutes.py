from ui.WebUI import WebUI
from flask import render_template, request
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo

class UpdateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/update_video_note')
    def update_video_note():
        return render_template("update/update_video_note.html", videos=WebUI.get_all_videos())

    @staticmethod
    @__app.route('/do_update_video_note', methods=['GET', 'POST'])
    def do_update_video_note():
        key, error = WebUI.validate_field("The video", "video")
        if key is None:
            return error
        video = MusicVideo.lookup(key)
        if video is None:
            return render_template(
                "error.html",
                message_header="Video does not exist!",
                message_body=f"The video {key} does not exist. Please choose another video and try again."
            )
        if "note" in request.form:
            note = request.form["note"].strip()
        else:
            note = ""
        video.update_note(note)
        return render_template("update/confirm_note_updated.html", video=video)

    @staticmethod
    @__app.route('/add_video_to_playlist')
    def add_video_to_playlist():
        return render_template(
            "update/add_video_to_playlist.html",
            videos=WebUI.get_all_videos(),
            playlists=WebUI.get_all_playlists()
        )

    @staticmethod
    @__app.route('/do_add_video_to_playlist', methods=['GET', 'POST'])
    def do_add_video_to_playlist():
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
        if video in playlist:
            return render_template(
                "error.html",
                message_header=f"The video is already in the playlist.",
                message_body=f"The video '{video.get_printable_key()}' is already in the playlist '{playlist.get_printable_key()}'."
            )
        playlist.append(video)
        return render_template("update/confirm_video_added_to_playlist.html", video=video, playlist=playlist)

    @staticmethod
    @__app.route("/remove_video_from_playlist")
    def remove_video_from_playlist():
        return render_template(
            "update/remove_video_from_playlist.html",
            videos=WebUI.get_all_videos(),
            playlists=WebUI.get_all_playlists()
        )

    @staticmethod
    @__app.route('/do_remove_video_from_playlist', methods=['GET', 'POST'])
    def do_remove_video_from_playlist():
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
        playlist_key, error = WebUI.validate_field("The playlist name", "playlist")
        if playlist_key is None:
            return error
        playlist = PlayList.lookup(playlist_key.lower())
        if playlist.get_name() == PlayList.ALL_VIDEOS:
            return render_template(
                "error.html",
                message_header=f"Cannot remove video.",
                message_body=f"You cannot remove videos from the '{PlayList.ALL_VIDEOS}' playlist."
            )
        if playlist is None:
            return render_template(
                "error.html",
                message_header=f"The playlist {playlist_key} was not found.",
                message_body=f"A playlist with the name '{playlist_key}' was not found. Please choose another playlist and try again."
            )
        if video not in playlist:
            return render_template(
                "error.html",
                message_header=f"The video is not in the playlist.",
                message_body=f"The video '{video.get_printable_key()}' is not in the playlist '{playlist.get_printable_key()}'."
            )
        playlist.remove(video)
        return render_template("update/confirm_video_removed_from_playlist.html", video=video, playlist=playlist)
