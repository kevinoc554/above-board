from flask import render_template, Blueprint
from aboveboard import mongo

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # sort through db in reverse order and get the 3 most recent additions
    games = mongo.db.games.find().hint([('$natural', -1)]).limit(3)
    games = list(games)
    # set ratings as a rounded average of the list of ints
    for game in games:
        game['rating'] = round(sum(game['rating'])/len(game['rating']))
    return render_template("home.html", games=games)
