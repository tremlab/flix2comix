"""all classes for interaction with the database.
"""
from flask_sqlalchemy import SQLAlchemy
from random import randint
# from datetime import date

db = SQLAlchemy()


class Movie(db.Model):
    """class for movie info. 
    """

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tmdb_id = db.Column(db.String(12), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    overview = db.Column(db.UnicodeText)
    tagline = db.Column(db.String(200))
    image_src = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    tmdb_rating = db.Column(db.Numeric(asdecimal=True))
    # below are deliberately non-normalized for efficiency
    bechdel = db.Column(db.Integer, nullable=False)
    visual = db.Column(db.Integer, nullable=False)
    linear = db.Column(db.Integer, nullable=False)
    cheerful = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    magical = db.Column(db.Integer, nullable=False)
    mature = db.Column(db.Integer, nullable=False)

    # implicit:
    # movie_ratings = db.relationship("MovieRating")
    # users = db.relationship("User", secondary=movie_ratings)

    @classmethod
    def get_randomized_movies(cls):
        """returns all movies in the database, but makes sure to RANDOMIZE.
        """
        movies = cls.query.all()
        movies_rand = []

        while len(movies) > 0:
            index = randint(0, len(movies) - 1)
            next_movie = movies.pop(index)
            movies_rand.append(next_movie)

        return movies_rand

    def __repr__(self):
        return """<movie_id: %i, title: %s, bec: %i, vis: %i, lin: %i, chr: %i,
        act: %i, mag: %i, mat: %i>""" % (self.movie_id, self.title, self.bechdel, self.visual, self.linear, self.cheerful, self.active, self.magical, self.mature)


class Comic(db.Model):
    """class for comic book info
    """

    __tablename__ = "comics"

    comic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn10 = db.Column(db.String(10))
    isbn13 = db.Column(db.String(13), unique=True)
    author = db.Column(db.String(100))
    artist = db.Column(db.String(100))  # if artist is not writer
    publisher = db.Column(db.String(50))
    title = db.Column(db.String(200))
    summary = db.Column(db.UnicodeText)
    # below are deliberately non-normalized for efficiency
    bechdel = db.Column(db.Integer, nullable=False) 
    visual = db.Column(db.Integer, nullable=False)
    linear = db.Column(db.Integer, nullable=False)
    cheerful = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    magical = db.Column(db.Integer, nullable=False)
    mature = db.Column(db.Integer, nullable=False)
    # implicit:
    # comic_recs = db.relationship("ComicRec")
    # user = db.relationship("User", secondary=comic_recs)

    def __repr__(self):
        return """<comic_id: %i, title: %s, bec: %i, vis: %i, lin: %i, chr: %i, 
        act: %i, mag: %i, mat: %i>""" % (self.comic_id, self.title, self.bechdel, self.visual, self.linear, self.cheerful, self.active, self.magical, self.mature)
  

class User(db.Model):
    """class for user info
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(30))
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # implicit:
    # movie_ratings = db.relationship("MovieRating")
    # comic_recs = db.relationship("ComicRec")
    # movies = db.relationship("Movie", secondary=movie_rating)
    # comics = db.relationship("Comic", secondary=comic_recs)

    def __repr__(self):
        return "<User_id: %i, email: %s>" % (self.user_id, self.email)


class MovieRating(db.Model):
    """class for rating for each movie the user rates (1-5)
    """

    __tablename__ = "movie_ratings"

    mr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    rated_at = db.Column(db.Date)
    ##### TEST #########
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id'), )

    user = db.relationship("User", backref="movie_ratings")
    movie = db.relationship("Movie", backref="movie_ratings")

    def __repr__(self):
        return """<mr_id: %i, user_id: %i, movie_id: %i,
        rating: %i>""" % (self.mr_id, self.user_id, self.movie_id, self.rating)


class ComicRec(db.Model):
    """class for comic recommendations to each user.
    """

    __tablename__ = "comic_recs"

    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.comic_id'), nullable=False)
    recd_at = db.Column(db.Date, nullable=False)
    user_read = db.Column(db.Boolean)
    user_rating = db.Column(db.Integer)  # 1-5

    __table_args__ = (db.UniqueConstraint('user_id', 'comic_id'), )

    user = db.relationship("User", backref="comic_recs")
    comic = db.relationship("Comic", backref="comic_recs")

    def __repr__(self):
        return "<cr_id: %i, user_id: %i, comic_id: %i>" % (self.cr_id, self.user_id, self.comic_id)

#___________________________________________________________________________
#___________________________________________________________________________


def connect_to_db(app, db_name="flix2comix"):
    """Connect to database."""
    db_path = 'postgresql:///%s' % (db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    """if run directly, allows for interaction with database.
    """

    from server import app
    connect_to_db(app)
    print "Connected to DB!"
