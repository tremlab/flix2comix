"""all classes for interaction with the database.
"""
from flask_sqlalchemy import SQLAlchemy
from random import randint
# from datetime import date

db = SQLAlchemy()


class Movie(db.Model):
    """class for movie info
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
    email = db.Column(db.String(50))
    password = db.Column(db.String(12))

    # implicit:
    # movie_ratings = db.relationship("MovieRating")
    # comic_recs = db.relationship("ComicRec")
    # movies = db.relationship("Movie", secondary=movie_rating)
    # comics = db.relationship("Comic", secondary=comic_recs)

    # def get_comic_rec(self):
    #     """user ratings will be dynamically called,
    #         since ratings may be added or changed over time.
    #         Calls user profile, then retruns comic object of best match.
    #     """
    #     #from rating data, get the aggregate preferences for this user.
    #     profile = MovieRating.get_profile(self.user_id)
    #     #from comic data, find the book whose profile most closely matches user's
    #     best_comic = ComicRec.get_user_match(profile, self.user_id)

    #     return best_comic


    def __repr__(self):
        return "User_id: %i, email: %s" % (self.user_id, self.email)


class MovieRating(db.Model):
    """class for rating for each movie the user rates (1-5)
    """

    __tablename__ = "movie_ratings"

    mr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  ##  -2 : 2
    rated_at = db.Column(db.Date)

    user = db.relationship("User", backref="movie_ratings")
    movie = db.relationship("Movie", backref="movie_ratings")

    # @classmethod
    # def get_profile(cls, user_id):
    #     """based on the user's movie ratings, calculate a preference profile.
    #         it works!!!!  :D
    #     """
    #     user_ratings = cls.query.filter_by(user_id = user_id).all()

    #     user_category_ratings = {
    #         "bechdel": 0,
    #         "visual": 0,
    #         "linear": 0,
    #         "cheerful": 0,
    #         "active": 0,
    #         "magical": 0,
    #         "mature": 0,
    #     }

    #     for r in user_ratings:
    #         #weight the category rating by how much the user liked the movie
    #         user_category_ratings["bechdel"] += (r.rating * r.movie.bechdel)
    #         user_category_ratings["visual"] += (r.rating * r.movie.visual)
    #         user_category_ratings["active"] += (r.rating * r.movie.active)
    #         user_category_ratings["linear"] += (r.rating * r.movie.linear)
    #         user_category_ratings["cheerful"] += (r.rating * r.movie.cheerful)
    #         user_category_ratings["magical"] += (r.rating * r.movie.magical)
    #         user_category_ratings["mature"] += (r.rating * r.movie.mature)

    #     #divide by # of ratings for average
    #     for category, score in user_category_ratings.items():
    #         user_category_ratings[category] /= len(user_ratings)
    #     #divide by 2 (highest score) to get back to scale
    #         user_category_ratings[category] /= 2

    #     return user_category_ratings

    def __repr__(self):
        return """"mr_id: %i, user_id: %i, movie_id: %i,
        rating: %i""" % (self.mr_ir, self.user_id, self.movie_id, self.rating)


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

    # @classmethod
    # def get_user_match(cls, user_profile, user_id_):
    #     """takes dictionary of user's category preferences, 
    #         finds comic book with the closest match, creates record in this table,
    #         returns book object.
    #     """
    #     #????????????????
    #     comics = Comic.query.filter(ComicRec.user_id != user_id_).join(ComicRec).all()
    #     ## query all COMICS that don't have a comic_rec with this user_id

    #     #to hold the results of each evaluation against user profile.
    #     ####list of tuples... (discprepancy, comic_id)
    #     match_ranking = []

    #     for comic in comics:
    #         #calculate the difference between user & this comic on each cat.
    #         visual_discr = user_profile["visual"] - comic.visual
    #         linear_discr = user_profile["linear"] - comic.linear
    #         active_discr = user_profile["active"] - comic.active
    #         cheerful_discr = user_profile["cheerful"] - comic.cheerful
    #         magical_discr = user_profile["magical"] - comic.magical
    #         mature_discr = user_profile["mature"] - comic.mature
    #         bechdel_discr = user_profile["bechdel"] - comic.bechdel

    #         total_discrepancy = (visual_discr +
    #                              linear_discr +
    #                              active_discr +
    #                              cheerful_discr +
    #                              magical_discr +
    #                              mature_discr +
    #                              bechdel_discr) / 6

    #         match_ranking.append((total_discrepancy, comic.comic_id))

    #     comics_sorted = match_ranking.sort()
    #     #from the best matching score, extract the comic_id
    #     best_match_comic = comics_sorted[0][1]
    #     #create record of this recommendation
    #     new_rec = ComicRec(user_id=user_id_, comic_id=comic_id, recd_at=date.today())
    #     db.session.add(new_rec)
    #     db.commit.all()
    #     #get the full object from the database
    #     best_comic = Comic.query.get(best_match_comic)

    #     return best_comic

    def __repr__(self):
        return "cr_id: %i, user_id: %i, comic_id: %i" % (cr_id, user_id, comic_id)

#___________________________________________________________________________
#___________________________________________________________________________


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