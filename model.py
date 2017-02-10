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
    bechdel = db.Column(db.Integer, nullable=False)
    # below are deliberately non-normalized for efficiency
    visual = db.Column(db.Integer, nullable=False)
    linear = db.Column(db.Integer, nullable=False)
    cheerful = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    mature = db.Column(db.Integer, nullable=False)

    # implicit:
    # movie_ratings = db.relationship("MovieRating")
    # users = db.relationship("User", secondary=movie_ratings)

    def __repr__():
        pass


class Comic(db.Model):
    """class for comic info
    """

    __tablename__ = "comics"

    comic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn10 = db.Column(db.String(10))
    isbn13 = db.Column(db.String(13), unique=True)
    author = db.Column(db.String(100))
    artist = db.Column(db.String(50))  # if artist is not writer
    publisher = db.Column(db.String(50))
    title = db.Column(db.String(200))
    summary = db.Column(db.UnicodeText)
    # below are deliberately non-normalized for efficiency
    bechdel = db.Column(db.Integer, nullable=False) 
    visual = db.Column(db.Integer, nullable=False)
    linear = db.Column(db.Integer, nullable=False)
    cheerful = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    mature = db.Column(db.Integer, nullable=False)
    # implicit:
    # comic_recs = db.relationship("ComicRec")
    # user = db.relationship("User", secondary=comic_recs)

    def __repr__():
        pass

class User(db.Model):
    """class for user info
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(12))

    # implicit:
    # movie_ratings = db.relationship("MovieRating")
    # comic_recs = db.relationship("ComicRec")
    # movies = db.relationship("Movie", secondary=movie_rating)
    # comics = db.relationship("Comic", secondary=comic_recs)

    # def get_rating_profile(self):
    #     """user ratings will be dynamically called,
    #         since ratings may be added or changed over time.
    #     """
    #     user = User.query.get(self.user_id)
    #     #list of movie ratings objects for this user
    #     ratings = user.movie_ratings

    #     user_category_ratings = {
    #         "bechdel": 0,
    #         "visual": 0,
    #         "linear": 0,
    #         "cheerful": 0,
    #         "active": 0,
    #         "mature": 0,
    #     }

    #     for r in ratings:
    #         #weight the category rating by how much the user liked the movie
    #         for category, score in user_category_ratings.items():
    #             score += (r.rating * r.movie.category)

    #     #divide by # of ratings for average
    #     for category, score in user_category_ratings.items():
    #         score = score / len(ratings)
    #     #divide by 5 (highest score) to get back to scale
    #         scores = score / 5

    #     return user_category_ratings


    def __repr__():
        pass


class MovieRating(db.Model):
    """collects the rating for each movie the user rates (1-5)
    """

    __tablename__ = "movie_ratings"

    mr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    rated_at = db.Column(db.Date)

    user = db.relationship("User", backref="movie_ratings")
    movie = db.relationship("Movie", backref="movie_ratings")

    def __repr__():
        pass


class ComicRec(db.Model):
    """class for comic recommendations to each user.
    """

    __tablename__ = "comic_recs"

    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.comic_id'), nullable=False)
    recd_at = db.Column(db.Date)
    user_read = db.Column(db.Boolean)
    user_rating = db.Column(db.Integer)  # 1-5

    user = db.relationship("User", backref="comic_recs")
    comic = db.relationship("Comic", backref="comic_recs")

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

    from server import app
    connect_to_db(app)
    print "Connected to DB!"