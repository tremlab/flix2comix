"""all classes for interaction for the database.
"""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class Movie(db.Model):
    """class for movie info
    """

    __tablename__ = "movies"

    tmdb_id = db.Column(db.String(12), primary_key=True)
    imdb_id = db.Column(db.String(20))
    overview = db.Column(db.UnicodeText) #blob???
    tagline = db.Column(db.String(200))
    image_src = db.Column(db.String(200))
    title = db.Column(db.String(200))
    tmdb_rating = db.Column(db.Numeric(asdecimal=True))
    tmdb_genre_list = db.Column(db.  ) ###?
    bechdel_rating = db.Column(db.Integer)

    # manually coded categories

    def __repr__():
        pass


class Comic(db.Model):
    """class for comic info
    """

    __tablename__ = "comics"

    isbn10 = db.Column(db.String(10), primary_key=True)
    isbn13 = db.Column(db.String(13), unique=True)
    author_list = db.Column(db.String(100))#
    #artist?
    publisher = db.Column(db.String(50))
    title = db.Column(db.String(200))
    summary = db.Column(db.UnicodeText)

    # manually coded categories

    def __repr__():
        pass

class User(db.Model):
    """class for user info
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(12))

    # calculated preferences for profile

    def __repr__():
        pass

class MovieRating(db.Model):
    """collects the rating for each movie the user rates (1-5)
    """

    __tablename__ = "movie_ratings"  

    mr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(users.user_id), nullable=False)
    tmdb_id = db.Column(db.String(12), ForeignKey(movies.tmdb_id), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5
    # date?

    def __repr__():
        pass

class ComicRec(db.Model):
    """class for comic recommendations to each user.
    """

    __tablename__ = "comic_recs"

    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(users.user_id), nullable=False)
    isbn10 = db.Column(db.String(12), ForeignKey(comics.isbn10), nullable=False)
    recommended_at = db.Column(db.Date)
    user_read = db.Column(Boolean)
    user_rating = db.Column(db.Integer)  # 1-5

    def __repr__():
        pass