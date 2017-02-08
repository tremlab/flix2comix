"""collect and format data to populate the database.
"""

import json
import requests
import isbnlib
import sys
import os

# pull api keys from environ (created from secrets file)
tmdb_key = os.environ["TMDB_KEY"]
tmdb_read = os.environ["TMDB_READ_TOKEN"]
isbn_key = os.environ["ISBN_KEY"]


def read_movielist(filename):
    """opens named file, returns a dictionary of all titles (key)
        & TMDB ids (value)
        input e.g. Jack+Reacher|999
    """
    movie_ids = {}

    with open(filename) as movie_file:
        for movie in movie_file:
            movie = movie.rstrip()
            title, tmdb_id = movie.split("|")
            movie_ids[title] = tmdb_id

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
    """takes a dictionary of title: tmdb_id,
    collects tmdb data on it (get_movie_tmdb),
    gleans valued data from the entire set,
    returns a list of dictionaries, ready for the db.
    """

    movies = []

    for mtitle, id in movie_ids.items():
        tmdb = get_movie_tmdb(id)

        movie = {}

        movie["tmdb_id"] = tmdb["id"]
        movie["imdb_id"] = tmdb["imdb_id"]
        movie["overview"] = tmdb["overview"]
        movie["tagline"] = tmdb["tagline"]
        movie["image_src"] = tmdb["poster_path"]  # figure out these paths??
        movie["title"] = tmdb["title"]
        movie["tmdb_rating"] = tmdb["vote_average"]
        movie["tmdb_genre_list"] = tmdb["genres"]
        # MPAA rating????

        # add on bechdel rating for each movie
        movie["bechdel_rating"] = get_bechdel_score(movie["imdb_id"])

        movies.append(movie)

    # LIST of all downloadable data on each movie as dictionary
    return movies

##########################
# Books

def read_comiclist(filename):
    """opens named file, returns a dicitionary of all titles (key)
        & value of a tuple with both ISBN10 & ISBN13
        input e.g. Nao+of+Brown|1906838429|9781906838423
    """
    comics_ids = {}

    with open(filename) as comic_file:
        for comic in comic_file:
            comic = comic.rstrip()
            title, ISBN10, ISBN13 = comic.split("|")
            comics_ids[title] = (ISBN10, ISBN13)

    return comics_ids

#  https://www.comics.org/ ?????
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

    for ctitle, ISBNs in comics_ids.items():
        ISBN10 = ISBNs[0]
        isbn = get_comic_by_isbn(ISBN10)

        comic = {}

        comic["isbn10"] = isbn["isbn10"]
        comic["isbn13"] = isbn["isbn13"]
        comic["author_list"] = isbn["author_data"]#   [0].get("name")
        #artist?
        comic["publisher"] = isbn["publisher_name"]
        comic["title"] = isbn["title"]
        comic["summary"] = isbn["summary"]  # figure out these paths??

        comics.append(comic)

    # LIST of all downloadable data on each comic as dictionary
    return comics


# if __name__ == '__main__':

#     movie_file = sys.args[1]
#     comic_file = sys.args[2]

#     movie_list = read_movielist(movies)
#     movies = process_movie_list(movie_list)

#     comic_list = read_comiclist(comic_file)
#     comics = process_comic_list(comic_list)

    # instantiate each list on their class and add to db