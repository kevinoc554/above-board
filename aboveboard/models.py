from aboveboard import app, mongo, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({"username": username})
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
        Overide get_id method provided by flask_login
        """
        return self.username

    def get_token(self, expires_sec=1800):
        """
        Creates a token using app's secretkey and user's unique username
        Expiry time can be set in secs, defaults to 30 mins
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.username}).decode('utf-8')

    @staticmethod
    def check_token(token):
        """
        Decodes the token, and returns the relevant user.
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            username = s.loads(token)['user_id']
        except Exception as e:
            print(e)
            return None
        return mongo.db.users.find_one({'username': username})

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Genre():
    """
    A class that represents a Genre of Game,
    and allows for db operations
    """

    def __init__(self, genre):
        """
        Initialize an instance of the User class
        """
        self.genre = genre

    @staticmethod
    def list_genres():
        genres = mongo.db.genres.find()
        genre_list = [g['genre'].title() for g in genres]
        return genre_list


class Mechanic():
    """
    A class that represents a Genre of Game,
    and allows for db operations
    """

    def __init__(self, mechanic):
        """
        Initialize an instance of the User class
        """
        self.mechanic = mechanic

    @staticmethod
    def list_mechanics():
        mechanics = mongo.db.mechanics.find()
        mechanic_list = [m['mechanics'].title() for m in mechanics]
        return mechanic_list
