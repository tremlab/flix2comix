"""Should I create and destroy the db before/after each test?
    difficult to stabilize data while testing.
"""


import analysis
import unittest
from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)


class flix2comixTest(unittest.TestCase):

    def test_get_profile_user3(self):
        """
        """
        profile3 = analysis.get_profile(3)
        assertEqual(profile3["linear"], -1)
        assertEqual(profile3["mature"], 0)

    def test_get_user_match3(self):
        """
        """
        comic = analysis.test_get_user_match(3)
        assertEqual(comic.title, "Why I Hate Saturn")

    # def test_process_user_rating(self):
    #     """
    #     """
    #     analysis.process_user_rating(10, 10, 2)
    #     r = MovieRating.query.filter(user_id=10, movie_id=10).one()
   
    #     assertEqual(r.rating, 2)

    def setUp(self):
        """connect to db? createdb???"""
        # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        # example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':

    from server import app
    connect_to_db(app, "MOCKflix2comix")
    print "Connected to DB!"

    unittest.main()



