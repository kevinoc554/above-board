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


if __name__ == '__main__':
    main()
