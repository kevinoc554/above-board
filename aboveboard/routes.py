from flask import (
    flash, render_template,
    redirect, request, url_for)
from aboveboard import app, mongo, bcrypt, mail
from aboveboard.forms import (RegistrationForm, LoginForm,
                              UpdateAccountForm, RequestResetForm,
                              ResetPasswordForm, AddGameForm,
                              SearchForm, EditGameForm)
from aboveboard.models import User, Genre, Mechanic, Game
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_pymongo import ObjectId
from flask_paginate import Pagination, get_page_args





















