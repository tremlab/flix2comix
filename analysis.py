from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from datetime import date
from flask import flash
from sqlalchemy.orm.exc import NoResultFound
import random


def get_random_movie(elimination_list, u_id):
    """takes in a list of movie_ids user has seen (from session),
        also checks for movies already rated (from db), then
        randomly picks a NEW movie for the user. -- returns movie object.
    """
    # list of all movie ids.
    all_movies = db.session.query(Movie.movie_id).all()
    all_movie_ids = []
    for movie in all_movies:
        all_movie_ids.append(movie[0])  # getting raw id out of tuple

    # list of movie_ids that were rated by this user
    movies_rated_objs = get_user_movies(u_id)
    movies_rated_ids = []
    for movie in movies_rated_objs:
        print movie
        movies_rated_ids.append(movie[1].movie_id)
    print "movies rated:", movies_rated_ids
    # elimination_list -- ids of movies user has SEEN but not RATED.

    avail_movies = []

    for movie in all_movie_ids:
        if movie not in elimination_list + movies_rated_ids:
            avail_movies.append(movie)
    print "movies not seen, not rated:", avail_movies
    # if user has seen & rated all the movies,
    # go back to seen, but unrated movies
    if avail_movies == []:
        for movie in all_movie_ids:
            if movie not in movies_rated_ids:
                avail_movies.append(movie)
    print "movies seen, but not rated", avail_movies
    #if user has rated all movies, return None
    if avail_movies == []:
        return None

    print "avaialable movies:", avail_movies
    choice_index = random.randint(0, len(avail_movies))
    print "choice_index", choice_index
    selected_movie_id = avail_movies[choice_index - 1]  # OB1
    print "movie_id", selected_movie_id
    #get the full movie object from db
    random_movie = Movie.query.get(selected_movie_id)

    return random_movie


def process_user_rating(u_id, mv, r):
    """given a user_id, movie_id, & user rating, determine if this is a NEW or
        UPDATING event, and handle accordingly.
    """
    try:
        # check if this user/movie combo already has a record in the db.
        this_rating = MovieRating.query.filter(MovieRating.user_id == u_id,
                                               MovieRating.movie_id == mv).one()
        # update to new rating value given by user
        this_rating.rating = r
        this_rating.rated_at = date.today()
        title = this_rating.movie.title
        update = "Updated your rating for %s" % (title)
        flash(update)
    except NoResultFound:
        mrating = MovieRating(user_id=u_id, movie_id=mv, rating=r, rated_at=date.today())
        db.session.add(mrating)

    db.session.commit()


#####DRY################????
def process_comic_rating(u_id, cm, r):
    """given a user_id, comic_id, & user rating, determine if this is a NEW or
        UPDATING event, and handle accordingly.
    """
    try:
        # check if this user/comic combo already has a record in the db.
        this_rating = ComicRec.query.filter(ComicRec.user_id == u_id,
                                               ComicRec.comic_id == cm).one()
        # update to new rating value given by user
        this_rating.user_rating = r
        #not tracking the date of user rating, only date recommnded.
        title = this_rating.comic.title
        print title
        update = "Updated your rating for %s" % (title)
        # flash(update)
    #in current workflow, never rating a movie that wasn't reocmmended. 
    except NoResultFound:
        c_rating = ComicRec(user_id=u_id, comic_id=cm, user_rating=r, recd_at=date.today())
        db.session.add(c_rating)

    db.session.commit()


def get_user_movies(u_id):
    """find all movies this user (by user_id) has rated.
        returns list of movie objects.
    """
    movies = db.session.query(MovieRating, Movie).join(Movie).filter(MovieRating.user_id == u_id).all()

    return movies


def get_user_comics(u_id):
    """find all comics that have been recommended to this user so far.
        return list of comic objects.
    """
    comics = db.session.query(ComicRec, Comic).join(Comic).filter(ComicRec.user_id == u_id).all()

    return comics


def get_profile(u_id):
    """based on the user's movie ratings, calculate a preference profile.
    """
    user_ratings = MovieRating.query.filter_by(user_id=u_id).all()

    user_category_ratings = {
        "bechdel": 0,
        "visual": 0,
        "linear": 0,
        "cheerful": 0,
        "active": 0,
        "magical": 0,
        "mature": 0,
    }

    for r in user_ratings:
        #weight the category rating by how much the user liked the movie
        user_category_ratings["bechdel"] += (r.rating * r.movie.bechdel)
        user_category_ratings["visual"] += (r.rating * r.movie.visual)
        user_category_ratings["active"] += (r.rating * r.movie.active)
        user_category_ratings["linear"] += (r.rating * r.movie.linear)
        user_category_ratings["cheerful"] += (r.rating * r.movie.cheerful)
        user_category_ratings["magical"] += (r.rating * r.movie.magical)
        user_category_ratings["mature"] += (r.rating * r.movie.mature)

    #divide by # of ratings for average
    for category, score in user_category_ratings.items():
        user_category_ratings[category] /= len(user_ratings)
    #divide by 2 (highest score) to get back to scale
        user_category_ratings[category] /= 2

    return user_category_ratings


def get_user_match(user_profile, u_id):
    """takes dictionary of user's category preferences, 
        finds comic book with the closest match, creates record in this table,
        returns book object.
    """

    # collect all comcis and their previous recommendations
    comics = Comic.query.all()
    previous_recs = ComicRec.query.filter(ComicRec.user_id == u_id)

    eliminate_comic_ids = []
    available_comics = []

    for rec in previous_recs:
        eliminate_comic_ids.append(rec.comic_id)
    for comic in comics:
        if comic.comic_id not in eliminate_comic_ids:
            available_comics.append(comic)

    #to hold the results of each evaluation against user profile.
    ####list of tuples... (discprepancy, comic_id)
    match_ranking = []

    for comic in available_comics:
        #calculate the difference between user & this comic on each cat.
        visual_discr = abs(user_profile["visual"] - comic.visual)
        linear_discr = abs(user_profile["linear"] - comic.linear)
        active_discr = abs(user_profile["active"] - comic.active)
        cheerful_discr = abs(user_profile["cheerful"] - comic.cheerful)
        magical_discr = abs(user_profile["magical"] - comic.magical)
        mature_discr = abs(user_profile["mature"] - comic.mature)
        bechdel_discr = abs(user_profile["bechdel"] - comic.bechdel)

        total_discrepancy = (visual_discr +
                             linear_discr +
                             active_discr +
                             cheerful_discr +
                             magical_discr +
                             mature_discr +
                             bechdel_discr) / 7.0

        match_ranking.append((total_discrepancy, comic.comic_id))

    match_ranking.sort()
    comics_sorted = match_ranking

    #from the best matching score, extract the comic_id
    best_match_comic = comics_sorted[0][1]

    #create record of this recommendation
    new_rec = ComicRec(user_id=u_id, comic_id=best_match_comic, recd_at=date.today())
    db.session.add(new_rec)
    db.session.commit()
    #get the full object from the database
    best_comic = Comic.query.get(best_match_comic)

    return best_comic


def get_comic_rec(u_id):
    """From user_id, calls for user profile to be genreated,
        then calls for single comic that best matches that profile.
        Returns book object.
    """
    #from rating data, get the aggregate preferences for this user.
    profile = get_profile(u_id)
    #from comic data, find the book whose profile most closely matches user's
    best_comic = get_user_match(profile, u_id)

    return best_comic

###################################################
### for testing - if run directly

if __name__ == '__main__':
    """if run directly, allows for interaction with database.
    """

    from server import app
    connect_to_db(app)
    print "Connected to DB!"
