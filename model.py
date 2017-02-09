"""all classes for interaction with the database.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    """class for movie info
    """

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tmdb_id = db.Column(db.String(12), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    overview = db.Column(db.UnicodeText) #blob???
    tagline = db.Column(db.String(200))
    image_src = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    tmdb_rating = db.Column(db.Numeric(asdecimal=True))
    bechdel_rating = db.Column(db.Integer, nullable=False)
    VISUAL = db.Column(db.Integer, nullable=False)
    LINEAR = db.Column(db.Integer, nullable=False)
    CHEERFUL = db.Column(db.Integer, nullable=False)
    ACTIVE = db.Column(db.Integer, nullable=False)
    MATURE = db.Column(db.Integer, nullable=False)

    # manually coded categories

    ratings = db.relationship("MovieRating")
    users = db.relationship("User", secondary="MovieRating")

    def __repr__():
        pass


class Comic(db.Model):
    """class for comic info
    """

    __tablename__ = "comics"

    comic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn10 = db.Column(db.String(10), primary_key=True)
    isbn13 = db.Column(db.String(13), unique=True)
    author = db.Column(db.String(100))
    artist = db.Column(db.String(50))  # if artist is not writer
    publisher = db.Column(db.String(50))
    title = db.Column(db.String(200))
    summary = db.Column(db.UnicodeText)

    # manually coded categories

    recs = db.relationship("ComicRec")
    user = db.relationship("User", secondary="ComicRec")

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

    ratings = db.relationship("MovieRating")
    recs = db.relationship("ComicRec")
    movies = db.relationship("Movie", secondary="MovieRating")
    comics = db.relationship("Comic", secondary="ComicRec")

    def __repr__():
        pass


class MovieRating(db.Model):
    """collects the rating for each movie the user rates (1-5)
    """

    __tablename__ = "movie_ratings"

    mr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.String(12), db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    rated_at = db.Column(db.Date)

    user = db.relationship("User")
    movie = db.relationship("Movie")

    def __repr__():
        pass


class ComicRec(db.Model):
    """class for comic recommendations to each user.
    """

    __tablename__ = "comic_recs"

    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.String(12), db.ForeignKey('comics.comic_id'), nullable=False)
    recd_at = db.Column(db.Date)
    user_read = db.Column(db.Boolean)
    user_rating = db.Column(db.Integer)  # 1-5

    user = db.relationship("User")
    comic = db.relationship("Comic")

    def __repr__():
        pass

def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flix2comix'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    """if run directly, allows for interaction with database.
    """

    from server im[port app
    connect_to_db(app)
    print "Connected to DB!"