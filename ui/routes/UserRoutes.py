from ui.WebUI import WebUI
from flask import render_template, request, session, redirect, url_for
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo
from logic.User import User


class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/login")
    def login():
        return render_template("user/login.html")

    @staticmethod
    @__app.route("/do_login", methods=["GET", "POST"])
    def do_login():
        username, error = WebUI.validate_field("Username", "username")
        if error is not None:
            return error
        password, error = WebUI.validate_field("Password", "password")
        if error is not None:
            return error
        type, error = WebUI.validate_field("Type", "type")
        if error is not None:
            return error
        user = User.read_user(username)
        if type == "login":
            if user is None:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt failed. Please check your account information and try again."
                )
            logged_in = user.verify_password(password)
            if not logged_in:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt failed. Please check your account information and try again."
                )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        elif type == "register":
            if user is not None:
                return render_template(
                    "error.html",
                    message_header="Registration Failed",
                    message_body="The registration attempt failed. Please check your account information and try again."
                )
            user = User(username, User.hash_password(password))
            user.add()
            # name, videos, thumbnail, description, user_key, playlist_map, save=False
            PlayList(
                PlayList.ALL_VIDEOS,
                [],
                "https://glassgirder.com/music_player/images/all_videos.jpg",
                f"All Videos for {username}",
                user.get_key(),
                {},
                save=True
            )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        else:
            return render_template(
                "error.html",
                message_header="Unknown Login Type",
                message_body="Login type must be login or register. Please check your account information and try again."
            )

    @staticmethod
    @__app.route("/logout")
    def logout():
        if "user" in session:
            WebUI.logout()
            del session["user"]
        return redirect(url_for("login"))
