"""server for flix2comix
"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template,
                   redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from sqlalchemy.orm.exc import NoResultFound

import analysis


app = Flask(__name__)

app.secret_key = "monkey"

app.jinja_env.endefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/register', methods=["GET"])
def display_register_form():

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def process_register_form():
    email = request.form.get("email")
    password = request.form.get("password")

    #Check if user already exists, if not create user and add to table
    try:
        user_check = User.query.filter_by(email=email).one()
        flash("Email already registered!")
        return render_template("register_form.html")
    except NoResultFound:
        user = User(email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.user_id
        flash("You are registered & logged in.")
        return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def display_login_form():
    """show the login form for exisitng users
    """

    return render_template("login_form.html")

@app.route('/login-validation', methods=["POST"])
def process_login_form():
    """confirm user's login, add cookie to session.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user_check = User.query.filter_by(email=email).one()
    except NoResultFound:
        flash("Email not found")
        return redirect("/login")

    # if user found, check if password matches
    if password == user_check.password:
        session['user_id'] = user_check.user_id
        flash("Logged in successfully")
        route = "/userpage/" + str(user_check.user_id)
        return redirect(route)
    else:
        flash("Wrong password!")
        return render_template("login_form.html")


@app.route('/logout')
def logout():
    del session['user_id']
    flash("Logged out successfully")
    return redirect("/")


@app.route('/movies')
def show_movies():
    """display the page in which user will rate movies.
    """
    movie_list = Movie.get_randomized_movies()
    return render_template("movies.html", movies=movie_list)


@app.route('/rate', methods=["POST"])
def submit_movie_ratings():
    """collect user's movie ratings, add info to database, send to comics page.
    """
    # must iterate through form, since we don't know how many repsonses.
    ratings = request.form
    user = session["user_id"]

    for mv, r in ratings.items():
        #convert from string response
        mv = int(mv)
        r = int(r)

        if r != 0:
            mrating = MovieRating(user_id=user, movie_id=mv, rating=r)
            db.session.add(mrating)
        ### need to double check if movie has been rated already....

    db.session.commit()

    return render_template("comic.html")

    pass

if __name__ == '__main__':

    #helps with debugging
    app.debug = True
    #not caching on reload
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    #use debug toolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')