from aboveboard import app, mongo
from flask_login import current_user
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

    @classmethod
    def setUpClass(cls):
        """
        Set up app in Testing mode, and disable WtForm's
        CSRF tokens and return dummy user data for tests.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def tearDownClass(cls):
        """
        Remove dummy user data from db after testing.
        """
        mongo.db.users.delete_one({'username': 'unittest'})

    def test_a_register_user(self):
        """
        Test POST route for registering users.
        Attempt to add dummy user data to database, and then checks
        for user in db. Should redirect to Home page on success.

        Expected results:
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

    def test_invalid_login(self):
        """
        Test behaviour of POST Login route when given invalid login details.
        Should reload the page and flash a message.

        Expected results:
        Response - 200
        Flashed message: 'Incorrect email or password, please try again.'
        """
        dummy_login_data = {
            'email': 'unit@toast.com',
            'password': 'unit-toast'
        }
        client = app.test_client(self)
        response = client.post('/login', data=dummy_login_data)
        html = response.get_data().decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incorrect email or password, please try again.', html)

    def test_zlogin_user(self):
        """
        Test behaviour of POST Login route when given valid login details.
        Should put set the user as current_user and redirect to the home page.

        Expected results:
        Response - 302
        current_user.username: 'unittest'
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            response = client.post('/login', data=dummy_login_data)
            self.assertEqual(current_user.username, 'unittest')
            self.assertEqual(response.status_code, 302)

    def test_zlogout_user(self):
        """
        Test logout route.
        Logs a dummy user in, then logs the user out.
        On successful logout, the user is redirected to Home,
        and current_user becomes the AnonymousUserMixin object
        so the current user is not authenticated.

        Expected results:
        Response - 302
        current_user.is_authenticated - False
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/logout')
            self.assertEqual(current_user.is_authenticated, False)
            self.assertEqual(response.status_code, 302)

    def test_profile_logged_in(self):
        """
        Test GET request to Profile route by logged in User.

        Expected results:
        Response - 200
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/profile')
            self.assertEqual(response.status_code, 200)

    def test_my_games_logged_in(self):
        """
        Test GET request to My Games route by logged in User.

        Expected results:
        Response - 200
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/my-games')
            self.assertEqual(response.status_code, 200)

    def test_login_logged_in(self):
        """
        Test GET request to Login route by logged in User.
        Should redirect to Home.

        Expected results:
        Response - 302
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/login')
            self.assertEqual(response.status_code, 302)

    def test_register_logged_in(self):
        """
        Test GET request to Register route by logged in User.
        Should redirect to Home.

        Expected results:
        Response - 302
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'unit-test'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/register')
            self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    main()
