"""server for flix2comix
"""

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template,
                   redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

app.secret_key = "monkey"

app.jinja_env.endefined = StrictUndefined

##### code :)

if __name__ == '__main__':

    #helps with debugging
    app.debug = True
    #not chaching on reload
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    #use debug toolbar
    DebugToolbarExtension(app)