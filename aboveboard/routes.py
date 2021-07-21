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
        exisiting_username = mongo.db.users.find_one(
            {"username": request.form.get('username')})
        exisiting_email = mongo.db.users.find_one(
            {"email": request.form.get('email')})
        if exisiting_username or exisiting_email:
            flash("Username or email address already in use", "warning")
            return redirect(url_for('register'))
        register = form.make_dict()
        new_user = User(**register)
        new_user.add_user()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)
