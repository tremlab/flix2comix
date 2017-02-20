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
        return redirect("/movies")


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
        return redirect("/movies")
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
    # must iterate through entire form, since we don't know how many repsonses.
    ratings = request.form
    u_id = session["user_id"]

    for mv, r in ratings.items():
        #convert from string response
        mv = int(mv)
        r = int(r)
        # only for movies rated (not 0, which is default)
        if r != 0:
            # recalibrating 1:5 stars, into -2:2 -- algorithm more accurate.
            r = r - 3
            # call function to handle each rating.
            analysis.process_user_rating(u_id, mv, r)

    return redirect("/comic")


@app.route('/update_rate', methods=["POST"])
def update_movie_ratings():
    """collect user's movie ratings, add info to database, reload user page.
    """
    ##############DRY??? refactor into rate??#######
    # must iterate through entire form, since we don't know how many repsonses.
    ratings = request.form
    u_id = session["user_id"]

    for mv, r in ratings.items():
        #convert from string response
        mv = int(mv)
        r = int(r)
        # only for movies rated (not 0, which is default)
        if r != 0:
            # recalibrating 1:5 stars, into -2:2 -- algorithm more accurate.
            r = r - 3
            # call function to handle each rating.
            analysis.process_user_rating(u_id, mv, r)

    return redirect("/user")


@app.route('/update_comic', methods=["POST"])
def update_comic_ratings():
    """collect user's comic ratings, add info to database, reload user page.
    """
    ##############DRY??? refactor into rate??#######
    # must iterate through entire form, since we don't know how many repsonses.
    ratings = request.form
    u_id = session["user_id"]

    for cm, r in ratings.items():
        #convert from string response
        cm = int(cm)
        r = int(r)
        # only for movies rated (not 0, which is default)
        if r != 0:
            # recalibrating 1:5 stars, into -2:2 -- algorithm more accurate.
            r = r - 3
            # call function to handle each rating.
            analysis.process_comic_rating(u_id, cm, r)

    return redirect("/user")

############# method post???
@app.route('/comic', methods=["POST", "GET"])
def show_comic():
    """display to the user all the info on their recommended comic.
        will load automatically after they rate movies,
        but they also may want to call again to get a 2nd, 3rd book.
        function makes sure not to recommend same book twice to same user. ;)
    """
    # handle if no user_id??
    u_id = session["user_id"]
    recommended_comic = analysis.get_comic_rec(u_id)

    return render_template("comics.html", comic=recommended_comic)


@app.route('/user')
def show_user_info():
    """show user nickname, email. reset password button?
        list of their comic recs so far, and edit.
        list of movie ratings so far, and edit.
    """
    # handle if no user_id??
    u_id = session["user_id"]
    user = User.query.get(u_id)
    movies = analysis.get_user_movies(u_id)
    comics = analysis.get_user_comics(u_id)

    return render_template("user.html", user=user, movies=movies, comics=comics)


##################################################

if __name__ == '__main__':

    #helps with debugging
    app.debug = True
    #not caching on reload
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    #use debug toolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')