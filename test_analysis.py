"""Should I create and destroy the db before/after each test?
    difficult to stabilize data while testing.
"""


import analysis
import unittest
import os
from model import (User, Movie, Comic, MovieRating, ComicRec,
                   connect_to_db, db)
from sqlalchemy.pool import NullPool



class flix2comixTest(unittest.TestCase):

    def test_get_profile_user3(self):
        """
        """
        profile3 = analysis.get_profile(3)
        self.assertEqual(profile3["linear"], -1)
        self.assertEqual(profile3["mature"], 0)

    def test_get_user_match3(self):
        """
        """
        profile3 = analysis.get_profile(3)
        comic = analysis.get_user_match(profile3, 3)
        self.assertEqual(comic.title, "Why I Hate Saturn")

    # def test_process_user_rating(self):
    #     """
    #     """
    #     analysis.process_user_rating(10, 10, 2)
    #     r = MovieRating.query.filter(user_id=10, movie_id=10).one()

    #     assertEqual(r.rating, 2)

    def setUp(self):
        """connect to db? createdb???"""
        # Connect to test database

        # Create tables and add sample data
        # os.system("dropdb testdb")

        # engine = create_engine(
        #   'postgresql+psycopg2://scott:tiger@localhost/test',
        #   poolclass=NullPool)
        
        os.system("createdb testdb")
        os.system("psql testdb < BACKUPflix2comix")

        connect_to_db(app, "postgresql:///testdb")
        print "connected to testdb"

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        # db.engine.dispose()  -- didn't work :(
        os.system("dropdb testdb")


if __name__ == '__main__':

    from server import app
    # connect_to_db(app, "MOCKflix2comix")
    # print "Connected to DB!"

    unittest.main()




