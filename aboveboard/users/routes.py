from flask import (
    flash, render_template,
    redirect, request, url_for, Blueprint)
from aboveboard import mongo, bcrypt
from aboveboard.models import User
from aboveboard.users.utils import send_password_reset
from aboveboard.users.forms import (RegistrationForm, LoginForm,
                                    UpdateAccountForm, RequestResetForm,
                                    ResetPasswordForm, AdminForm)
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        register = form.make_dict()
        new_user = User(**register)
        new_user.add_user()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        find_user = mongo.db.users.find_one({'email': form.email.data})
        check_password = False
        if find_user:
            check_password = bcrypt.check_password_hash(
                find_user['password'], form.password.data)
        if find_user and check_password:
            user = User(**find_user)
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash('Incorrect email or password, please try again.', 'warning')

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out!', 'success')
    else:
        flash('You are not currently logged in.', 'info')
    return redirect(url_for('main.home'))


@users.route("/profile", methods=["GET", "POST"])
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
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        user = mongo.db.users.find_one({'username': current_user.username})
        form.fname.data = user['fname']
        form.lname.data = user['lname']
        form.email.data = user['email']

    return render_template('profile.html', title='Profile', form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        find_user = mongo.db.users.find_one({'email': form.email.data})
        user = User(**find_user)
        send_password_reset(user)
        flash(
            'An email with instructions to reset your password has been sent.',
            'success')
        return redirect(url_for('users.login'))
    return render_template('request-reset.html',
                           title='Request Password Reset', form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.check_token(token)
    if not user:
        flash('Unable to proceed. Please try again.', 'warning')
        return redirect(url_for('users.request_reset'))
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
        return redirect(url_for('users.login'))

    return render_template('reset-token.html', title='Reset Password',
                           form=form)


@users.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.username != 'admin':
        flash('You do not have permission to do that', 'warning')
        return redirect(url_for('main.home'))
    form = AdminForm()
    if form.validate_on_submit():
        if form.genre.data:
            mongo.db.genres.insert_one({'genre': form.genre.data})
        if form.mechanics.data:
            mongo.db.mechanics.insert_one({'mechanics': form.mechanics.data})
        flash('Category updated', 'success')
        return redirect(url_for('users.admin'))
    return render_template('admin.html', form=form, title='Admin')
