import json
import requests
import isbnlib
import sys
import os

# pull api keys from environ (created form secrets file)
tmdb_key = os.environ["TMDB_KEY"]
tmdb_read = os.environ["TMDB_READ_TOKEN"]
isbn_key = os.environ["ISBN_KEY"]


def read_movielist(filename):
    """opens named file, returns a dicitonary of all titles (key)
        & TMDB ids (value)
        e.g. Jack+Reacher|999
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
    # bechdel site requires the leading r letters be dropped
    bechdel_id = imdb_id[2:]

    bechdel_by_id = "http://bechdeltest.com/api/v1/getMovieByImdbId?imdbid=" + bechdel_id

    r = requests.get(bechdel_by_id)
    bechdel_data = r.json()
    bechdel_score = bechdel_data["rating"]
    
    return bechdel_score


def process_movie_list(movie_ids):
    """takes a dictionary of title[tmdb_id],
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

        movie["bechdel_rating"] = get_bechdel_score(movie["imdb_id"])

        movies.append(movie)

    # LIST of all data re
    return movies


# https://api.themoviedb.org/3/search/movie?api_key=e3d0fc958b1142490f250b376de9e820&query=Jack+Reacher
# https://api.themoviedb.org/3/search/movie?api_key=e3d0fc958b1142490f250b376de9e820&query=Jack+Reacher


# example API request TMDB:
# https://api.themoviedb.org/3/movie/343611?api_key={api_key}  ---search by movie id
# Our current limits are 40 requests every 10 seconds
# https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=Jack+Reacher search by title

# borrowed code for OMDB  ... need to address titles with spaces!!!

#### for single request:
# import json, requests
# url = "http://www.omdbapi.com/?t=scream"
# response = requests.get(url)
# python_dictionary_values = json.loads(response.text)


#### for multiple movies from file:
# movies = {}
# import json, requests
# baseurl = "http://omdbapi.com/?t=" #only submitting the title parameter
# with open("movies.txt", "r") as fin:
#      for line in fin:
#          movieTitle = line.rstrip("\n") # get rid of newline characters
#          response = requests.get(url + movieTitle)
#          if response.status_code == 200:
#               movies[movieTitle] = json.loads(response.text)
#          else:
#               raise ValueError("Bad request!")
# print movies['scream']