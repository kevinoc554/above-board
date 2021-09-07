from flask import (
    flash, render_template,
    redirect, request, url_for)
from aboveboard import app, mongo, bcrypt, mail
from aboveboard.forms import (RegistrationForm, LoginForm,
                              UpdateAccountForm, RequestResetForm,
                              ResetPasswordForm, AddGameForm)
from aboveboard.models import User, Genre, Mechanic, Game
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


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
        mongo.db.users.update_one({'username': current_user.username},
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


def send_password_reset(requester):
    token = requester.get_token()
    msg = Message('Password Reset Request',
                  sender='noreply@aboveboardgamedb.com',
                  recipients=[requester.email])
    msg.html = f'''<p>Hi {requester.fname},</p>
    <p>To reset your password,
    <a href="{url_for('reset_token', token=token, _external=True)}">
    click here</a></p>
    If you did not make this request then simply ignore this email
    and no changes will be made.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        find_user = mongo.db.users.find_one({'email': form.email.data})
        user = User(**find_user)
        send_password_reset(user)
        flash(
            'An email with instructions to reset your password has been sent.',
            'success')
        return redirect(url_for('login'))
    return render_template('request-reset.html',
                           title='Request Password Reset', form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.check_token(token)
    if not user:
        flash('Unable to proceed. Please try again.', 'warning')
        return redirect(url_for('request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        mongo.db.users.update({'username': user['username']},
                              {'$set': {
                                  'password': new_password
                              }
        })
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset-token.html', title='Reset Password',
                           form=form)


@app.route("/all-games")
def all_games():
    games = mongo.db.games.find()
    return render_template("all-games.html", games=games, title='All Games')


@app.route("/all-games/<gameid>")
def view_game(gameid):
    return render_template("view-game.html", title='GAME TITLE')


@app.route("/add-game", methods=["GET", "POST"])
@login_required
def add_game():
    form = AddGameForm()
    placehold = 'https://via.placeholder.com/250x200?text=No+Box+Art+Provided'
    base_list = ['Choose an Option']
    list_of_genres = Genre.list_genres()
    list_of_mechanics = Mechanic.list_mechanics()
    form.genre.choices = base_list + list_of_genres
    form.mechanics.choices = base_list + list_of_mechanics
    if form.validate_on_submit():
        if form.image_link.data == '':
            form.image_link.data = placehold
        form_data = form.make_dict()
        new_game = Game(**form_data)
        new_game.add_game(current_user)
        flash('Game Successfully Added!', 'success')
        return redirect(url_for('all_games'))
    return render_template("add-game.html", form=form, title="Add A Game")


@app.route("/my-games")
@login_required
def my_games():
    games = mongo.db.games.find({'added_by': current_user.username})
    return render_template('my-games.html', title='My Games', games=games)
