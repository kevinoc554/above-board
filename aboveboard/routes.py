from flask import (
    flash, render_template,
    redirect, request, url_for)
from aboveboard import app, mongo, bcrypt
from aboveboard.forms import (RegistrationForm, LoginForm,
                              UpdateAccountForm, RequestResetForm)
from aboveboard.models import User
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        find_user = mongo.db.users.find_one({'email': form.email.data})
        check_password = False
        if find_user:
            check_password = bcrypt.check_password_hash(
                find_user['password'], form.password.data)
        if find_user and check_password:
            user = User(**find_user)
            login_user(user)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Incorrect email or password, please try again.', 'warning')

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out!', 'success')
    else:
        flash('You are not currently logged in.', 'info')
    return redirect(url_for('home'))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        mongo.db.users.update({'username': current_user.username},
                              {'$set': {
                                  'fname': form.fname.data,
                                  'lname': form.lname.data,
                                  'email': form.email.data
                              }
        })
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        user = mongo.db.users.find_one({'username': current_user.username})
        form.fname.data = user['fname']
        form.lname.data = user['lname']
        form.email.data = user['email']

    return render_template('profile.html', title='Profile', form=form)


@app.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    form = RequestResetForm()
    return render_template('request-reset.html',
                           title='Request Password Reset', form=form)


@app.route("/my-games")
@login_required
def my_games():
    return render_template('my-games.html', title='Profile')
