import unittest
from server import app


class FlaskTests(unittest.TestCase):

    def test_homepage_ok(self):
        """homepage loading correctly?"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Comics are for grownups too!</h3>', result.data)

    def test_movie(self):
        result = self.client.get('/movies', follow_redirects=True)

        self.assertIn("Please rate at least", result.data)



    # BAD!! don't test database here!!!!
    # def test_login(self):
    #     result = self.client.post('/login-validation',
    #                               data={'email': 'monkey@pants.com', 'password': 'boo'},
    #                               follow_redirects=True)
    #     self.assertIn("Logged in successfully", result.data)

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


if __name__ == '__main__':
    unittest.main()
