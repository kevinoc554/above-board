from flask import (
    flash, render_template,
    redirect, request, url_for, Blueprint)
from aboveboard import mongo
from aboveboard.games.utils import PER_PAGE, convert_to_pagination, avg_ratings
from aboveboard.games.forms import AddGameForm, SearchForm, EditGameForm
from aboveboard.models import Genre, Mechanic, Game
from flask_login import current_user, login_required
from flask_pymongo import ObjectId

games = Blueprint('games', __name__)


@games.route("/all-games", methods=["GET", "POST"])
def all_games():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        games = Game.get_searched_games(query)
    else:
        games = Game.get_all_games()
    games = list(games)
    # set ratings as a rounded average of the list of ints
    for game in games:
        game['rating'] = round(sum(game['rating'])/len(game['rating']))
    games = sorted(games, key=lambda i: i['title'])
    pagination, games_paginated = convert_to_pagination(
        games, PER_PAGE, "page", "per_page")
    return render_template("all-games.html",
                           games=games_paginated,
                           form=form,
                           pagination=pagination,
                           title='All Games')


@games.route("/my-games", methods=["GET", "POST"])
@login_required
def my_games():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        search_all_games = Game.get_searched_games(query)
        games = [game for game in search_all_games
                 if game['added_by'] == current_user.username]

    else:
        search_my_games = Game.get_my_games(current_user)
        games = list(search_my_games)
    for game in games:
        game['rating'] = round(sum(game['rating'])/len(game['rating']))
    games = sorted(games, key=lambda i: i['title'])
    pagination, games_paginated = convert_to_pagination(
        games, PER_PAGE, "page", "per_page")
    return render_template('my-games.html', title='My Games',
                           games=games_paginated, pagination=pagination,
                           form=form)


@games.route("/view-game/<gameid>", methods=["GET", "POST"])
def view_game(gameid):
    if request.method == 'POST':
        if current_user.is_authenticated:
            new_rating = request.form.get('rating')
            new_rating = [int(new_rating)]
            game = mongo.db.games.find_one({"_id": ObjectId(gameid)})
            new_rating = game['rating'] + new_rating
            mongo.db.games.update_one(
                {"_id": ObjectId(gameid)},
                {'$set': {'rating': new_rating}})
            flash('Game rated!', 'success')
            return redirect(url_for('games.all_games'))
        else:
            flash('You do not have permission to do that.', 'warning')
            return redirect(url_for('games.all_games'))
    ref = request.referrer
    try:
        game = Game.get_one_game(gameid)
        game_as_list = list(game)
        if len(game_as_list) == 0:
            flash('Game could not be found, or does not exist', 'warning')
            return redirect(url_for('games.all_games'))
        avg_rating, num_ratings = avg_ratings(game_as_list[0]['rating'])
        return render_template("view-game.html",
                               game=game_as_list,
                               ref=ref,
                               rating=avg_rating,
                               num_ratings=num_ratings,
                               title='Game Info')
    except Exception:
        flash('Game could not be found, or does not exist', 'warning')
        return redirect(url_for('games.all_games'))


@games.route("/add-game", methods=["GET", "POST"])
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
        form_data['added_by'] = current_user.username
        new_game = Game(**form_data)
        new_game.add_game(current_user)
        flash('Game Successfully Added!', 'success')
        return redirect(url_for('games.all_games'))
    return render_template("add-game.html", form=form, title="Add A Game")


@games.route("/delete-game/<gameid>")
@login_required
def delete_game(gameid):
    try:
        find_game = mongo.db.games.find_one({"_id": ObjectId(gameid)})
        game = Game(**find_game)
        users = [game.added_by, 'admin']
        if current_user.username in users:
            Game.delete_one_game(gameid)
            flash('Game has been deleted!', 'success')
            return redirect(url_for('games.all_games'))
        else:
            flash('You do not have permission to delete that game', 'warning')
            return redirect(url_for('games.all_games'))
    except Exception:
        flash('That game could not be found!', 'warning')
        return redirect(url_for('games.all_games'))


@games.route("/edit-game/<gameid>", methods=["GET", "POST"])
@login_required
def edit_game(gameid):
    game = mongo.db.games.find_one({"_id": ObjectId(gameid)})
    users = [game['added_by'], 'admin']
    if current_user.username not in users:
        flash('You do not have permission to do that.', 'warning')
        return redirect(url_for('games.all_games'))
    form = EditGameForm()
    if form.validate_on_submit():
        changes = form.collect_changes()
        mongo.db.games.update_one({'_id': ObjectId(gameid)},
                                  {'$set': changes})
        flash('Game info edited!', 'success')
        return redirect(url_for('games.all_games'))

    elif request.method == 'GET':
        form.set_form_data(game)

    return render_template('edit-game.html', form=form)
