"""
"""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class Movie(db.Model):
    """class for movie info
    """

    __tablename__ = "movies"

    tmdb_id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.  )
    overview = db.Column(db.  )
    tagline = db.Column(db.  )
    image_src = db.Column(db.  )
    title = db.Column(db.  )
    tmdb_rating = db.Column(db.  )
    tmdb_genre_list = db.Column(db.  )
    bechdel_rating = db.Column(db.  )

    def __repr__():
        pass