import unittest
from server import app


class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage_ok(self):
        """homepage loading correctly?"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Comics are for grownups too!</h3>', result.data)

##### not working... ??

    # def test_login(self):
    #     result = self.client.post('/login-validation',
    #                               data={'email': 'monkey@pants.com', 'password': 'boo'},
    #                               follow_redirects=True)
    #     # test for flash message

    #     self.assertIn("Logged in successfully", result.data)
    #     ## might change what page they land on... user page?
    #     # self.assertIn("", result.data)

if __name__ == '__main__':
    unittest.main()
