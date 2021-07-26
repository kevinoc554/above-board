from aboveboard import mongo, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(username):
    user = mongo.db.Users.find_one({"username": username})
    if not user:
        return None
    return User(**user)


class User(UserMixin):
    """
    A class that represents a User,
    and allows for the relevant db operations
    """

    def __init__(self, fname, lname, username, email, password, _id=None):
        """
        Initialize an instance of the User class
        """
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password

    def get_info(self):
        """
        Convert User instance to dict to facilitate adding to db
        """
        info = {
            "fname": self.fname,
            "lname": self.lname,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return info

    def add_user(self):
        """
        Add user data to db.
        Uses get_info to convert User instance to dict.
        """
        mongo.db.users.insert_one(self.get_info())

    def get_id(self):
        """
        Get a user by username
        Overide get_id method provided by UserMixin
        """
        return self.username

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
