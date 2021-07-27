from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from aboveboard import app, mongo, bcrypt
from aboveboard.forms import RegistrationForm, LoginForm
from aboveboard.models import User
from flask_login import login_user, current_user


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        register = form.make_dict()
        new_user = User(**register)
        new_user.add_user()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        find_user = mongo.db.users.find_one({'email': form.email.data})
        check_password = bcrypt.check_password_hash(
            find_user['password'], form.password.data)
        if find_user and check_password:
            user = User(**find_user)
            print(user)
            login_user(user)
            print(current_user)
            flash('You have been logged in!', 'success')
            # return redirect(url_for('home'))
        else:
            flash('Incorrect email or password, please try again.', 'warning')

    return render_template("login.html", title="Login", form=form)
