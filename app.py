import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Classes
class User():
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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Routes


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/all_games")
def all_games():
    games = mongo.db.games.find()
    return render_template("all-games.html", games=games, title='All Games')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # register = {
        #     "fname": request.form.get("fname"),
        #     "lname": request.form.get("lname"),
        #     "username": request.form.get("username"),
        #     "email": request.form.get("email"),
        #     "password": request.form.get("password")
        # }
        register = form.make_dict()
        new_user = User(**register)
        print(repr(new_user))
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
