from ui.WebUI import WebUI
from flask import render_template, request, session, redirect, url_for
from logic.PlayList import PlayList
from logic.MusicVideo import MusicVideo
from logic.PerformanceVideo import PerformanceVideo
from logic.User import User


class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/get_user")
    def get_user():
        if "username" in session:
            return session["username"]
        return "None"

    @staticmethod
    @__app.route("/set_user")
    def set_user():
        if "username" in request.args:
            session["username"] = request.args["username"]
            return "User set."
        if "username" in session:
            del session["username"]
        return "User cleared"

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
        user = User.read_user(username)
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
        session["user"] = user
        return redirect(url_for("homepage"))

    @staticmethod
    @__app.route("/logout")
    def logout():
        if "user" in session:
            del session["user"]
        return redirect(url_for("login"))
