import bcrypt


class User:
    __username = ""
    __hash = ""

    def __init__(self, username, hash):
        self.__username = username
        self.__hash = hash

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "username": self.__username,
            "hash": self.__hash
        }

    @classmethod
    def build(cls, dict):
        return cls(dict["username"], dict["hash"])

    def get_key(self):
        return self.__username.lower()

    def get_username(self):
        return self.__username

    def get_hash(self):
        return self.__hash

    @staticmethod
    def read_user(username):
        from data.Database import Database

        return Database.read_user(username)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.__hash)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt(13)
        hash = bcrypt.hashpw(password.encode(), salt)
        return hash

    def add(self):
        from data.Database import Database

        Database.add_user(self)