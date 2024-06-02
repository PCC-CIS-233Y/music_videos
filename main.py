from ui.WebUI import WebUI
from logic.UserState import UserState


if __name__ == '__main__':
    from data.Database import Database

    # WebUI.init()
    WebUI.run()
    # user = Database.read_user("Mighty Mouse")
    # user_state = UserState(user)
    # print(user_state)