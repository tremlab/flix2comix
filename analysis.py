from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from flask_sqlalchemy import SQLAlchemy
from datetime import date
# from server import app



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
    comics = db.session.query(Comic, ComicRec).outerjoin(ComicRec).all()

    available_comics = []
    #eliminate any comics that have ALREADY been recommended to this person.
    for comic, rec in comics:
        if rec is not None:
            if rec.user_id != u_id:
                available_comics.append(comic)
        else:
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
