from aboveboard import app
from unittest import TestCase, main


class TestGetRoutes(TestCase):
    """
    Unit tests for basic GET routes.
    """

    def test_home(self):
        """
        Test GET requests to Home route.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_variant(self):
        """
        Test GET requests to Home route if accessed using '/home',
        rather than '/'.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_all_games(self):
        """
        Test GET requests to All Games route.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/all-games')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        Test GET requests to Login route.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Test GET requests to Register route.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        """
        Test GET requests to Profile route, for a user that is not logged in.
        Should redirect to Login route as login is required.

        Expected Results:
        Response - 302
        """
        client = app.test_client(self)
        response = client.get('/profile')
        self.assertEqual(response.status_code, 302)

    def test_my_games(self):
        """
        Test GET requests to My Games route, for a user that is not logged in.
        Should redirect to Login route as login is required.

        Expected Results:
        Response - 302
        """
        client = app.test_client(self)
        response = client.get('/my-games')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    main()
