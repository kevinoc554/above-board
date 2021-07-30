from aboveboard import app, mongo
from unittest import TestCase, main


class TestGetRoutes(TestCase):
    """
    Unit tests for basic GET routes.
    """

    def setUp(self):
        """
        Set up app in Testing mode
        """
        app.config['TESTING'] = True

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


class TestUserRoutes(TestCase):
    """
    Unit tests for routes and actions that require a User
    """

    def setUp(self):
        """
        Set up app in Testing mode, and disable WtForm's
        CSRF tokens and return dummy user data for tests.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        """
        Remove dummy user data from db after testing.
        """
        mongo.db.users.delete_one({'username': 'unittest'})

    def test_register_user(self):
        """
        Test POST route for registering users.
        Attempt to add dummy user data to database, and then checks
        for user in db. Should redirect to Home page on success.

        Expected response:
        Response - 302
        User found in db.
        """
        dummy_user_data = {
            "fname": 'Unit',
            "lname": 'test',
            "username": 'unittest',
            "email": 'unit@test.com',
            "password": 'unit-test',
            "confirm": 'unit-test'
        }
        client = app.test_client(self)
        response = client.post('/register', data=dummy_user_data)
        check_user = mongo.db.users.find_one({'username': 'unittest'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(check_user)


if __name__ == '__main__':
    main()
