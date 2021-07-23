from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from aboveboard import app, mongo
from aboveboard.forms import RegistrationForm
from aboveboard.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/all-games")
def all_games():
    games = mongo.db.games.find()
    return render_template("all-games.html", games=games, title='All Games')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        register = form.make_dict()
        new_user = User(**register)
        new_user.add_user()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)
