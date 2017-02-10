"""collect and format data to populate the database.
"""

import json
import requests
import isbnlib
import sys
import os
from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from server import app

# pull api keys from environ (created from secrets file)
tmdb_key = os.environ["TMDB_KEY"]
tmdb_read = os.environ["TMDB_READ_TOKEN"]
isbn_key = os.environ["ISBN_KEY"]


def read_movie_list(filename):
    """opens named file, returns a dictionary of all titles (key)
        & key as a list of: tmdb_id, catogories
        input e.g. Avatar|19995|2|3|3|3|5
    """
    movie_ids = {}

    with open(filename) as movie_file:
        for movie in movie_file:
            movie = movie.rstrip()

            title, tmdb_id, visual, linear, cheerful, active, mature = movie.split("|")

            movie_ids[title] = [tmdb_id,
                                visual,
                                linear,
                                cheerful,
                                active,
                                mature
                                ]

    return movie_ids


def get_movie_tmdb(movie_id):
    """takes a tmdb id string (numbers as string), sends a request to tmdb,
        converts each json response to a dictionary and returns it.
    """

    tmdb_request_by_id = "https://api.themoviedb.org/3/movie/" + movie_id + "?api_key=" + tmdb_key
    r = requests.get(tmdb_request_by_id)
    movie_data = r.json()

    return movie_data


def get_bechdel_score(imdb_id):
    """movies only! pass in imdb_id as string, returns score as string.
    """
    # bechdel site requires the leading 2 letters be dropped
    bechdel_id = imdb_id[2:]

    bechdel_by_id = "http://bechdeltest.com/api/v1/getMovieByImdbId?imdbid=" + bechdel_id

    r = requests.get(bechdel_by_id)
    bechdel_data = r.json()
    bechdel_score = bechdel_data["rating"]
    
    return bechdel_score


#bring over manual ratings too?  or handle separately? from read file...
def process_movie_list(movie_ids):
    """takes a dictionary of title: list of values,
    collects tmdb data on it (get_movie_tmdb),
    gleans valued data from the entire set,
    and returns a list of dictionaries, ready for the db.
    """

    movies = []

    for mtitle, data in movie_ids.items():
        tmdb = get_movie_tmdb(data[0])
        movie = {}

        # pulling data from tmdb object
        movie["tmdb_id"] = tmdb["id"]
        movie["imdb_id"] = tmdb["imdb_id"]
        movie["overview"] = tmdb["overview"]
        movie["tagline"] = tmdb["tagline"]
        movie["image_src"] = tmdb["poster_path"]  # figure out these paths??
        movie["title"] = tmdb["title"]
        movie["tmdb_rating"] = tmdb["vote_average"]
        # pulling data from bechdel test object
        movie["bechdel"] = int(get_bechdel_score(movie["imdb_id"]))
        #pulling data directly from movie dicitionary (hard-coded)
        movie["visual"] = int(data[1])
        movie["linear"] = int(data[2])
        movie["cheerful"] = int(data[3])
        movie["active"] = int(data[4])
        movie["mature"] = int(data[5])

        movies.append(movie)

    # LIST of all downloadable data on each movie as dictionary
    return movies

##########################
# Books

def read_comic_list(filename):
    """opens named file, returns a dicitionary of all titles (key)
        & value as list of ISBN10, and catgory data 
        input e.g. The Nao of Brown|1906838429|9781906838423|3|6|8|8|3
    """
    comics_ids = {}

    with open(filename) as comic_file:
        for comic in comic_file:
            comic = comic.rstrip()
            comic = comic.split("|")
            #too many to unpack in same line :(
            title = comic[0]
            ISBN10 = comic[1]
            bech = comic[2]
            visual = comic[3]
            linear = comic[4]
            cheerful = comic[5]
            active = comic[6]
            mature = comic[7]

            comics_ids[title] = [ISBN10,
                                 bech,
                                 visual,
                                 linear,
                                 cheerful,
                                 active,
                                 mature
                                 ]

    return comics_ids


def get_comic_by_isbn(isbn):
    """takes an isbn id string (numbers as string), sends a request to isbndb,
        converts each json response to a dictionary and returns it.
    """

    isbn_request = "http://isbndb.com/api/v2/json/" + isbn_key + "/book/" + isbn 
    r = requests.get(isbn_request)
    comic = r.json()
    comic_data = comic['data'][0]

    return comic_data


def process_comic_list(comics_ids):
    """takes a dictionary of title:(ISBN10,ISBN13),
    collects ISBN data on it (get_comic_by_isbn),
    gleans valued data from the entire set,
    returns a list of dictionaries, ready for the db.
    """

    comics = []

    for title, data in comics_ids.items():
        ISBN10 = data[0]
        isbn = get_comic_by_isbn(ISBN10)

        comic = {}

        # catching error - some author data is missing form the API :(
        if isbn["author_data"] == []:
            comic["author"] = ""
        else:
            comic["author"] = isbn["author_data"][0].get("name")

        comic["isbn10"] = isbn["isbn10"]
        comic["isbn13"] = isbn["isbn13"]
        comic["publisher"] = isbn["publisher_name"]
        comic["title"] = isbn["title"]
        comic["summary"] = isbn["summary"] 
        #artist?
        #pulling data dirctly from movie dicitonary (hard-coded)
        comic["bechdel"] = int(data[1])
        comic["visual"] = int(data[2])
        comic["linear"] = int(data[3])
        comic["cheerful"] = int(data[4])
        comic["active"] = int(data[5])
        comic["mature"] = int(data[6])

        comics.append(comic)

    # LIST of all downloadable data on each comic as dictionary
    return comics


if __name__ == '__main__':
    """connect to database, run api requests, instantiate
        objects, add to db.
    """
    connect_to_db(app)

    db.create_all()

    movie_file = sys.argv[1]
    comic_file = sys.argv[2]

    movie_list = read_movie_list(movie_file)
    movies = process_movie_list(movie_list)

    comic_list = read_comic_list(comic_file)
    comics = process_comic_list(comic_list)

    # instatiate and add movies to db
    for c in comics:

        comic = Comic(
            isbn10=c["isbn10"],
            isbn13=c["isbn13"],
            author=c["author"],
            publisher=c["publisher"],
            summary=c["summary"],
            title=c["title"],
            bechdel=c["bechdel"],
            visual=c["visual"],
            linear=c["linear"],
            cheerful=c["cheerful"],
            active=c["active"],
            mature=c["mature"]
            )

        db.session.add(comic)

    db.session.commit()

    # instatiate and add movies to db
    for m in movies:
        movie = Movie(
            tmdb_id=m["tmdb_id"],
            imdb_id=m["imdb_id"],
            overview=m["overview"],
            tagline=m["tagline"],
            image_src=m["image_src"],
            title=m["title"],
            tmdb_rating=m["tmdb_rating"],
            bechdel=m["bechdel"],
            visual=m["visual"],
            linear=m["linear"],
            cheerful=m["cheerful"],
            active=m["active"],
            mature=m["mature"]
            )

        db.session.add(movie)

    db.session.commit()

