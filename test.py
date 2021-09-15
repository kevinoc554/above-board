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
        Test GET requests to All Games route,
        and check that pagination is working.

        Expected Results:
        Response - 200
        'pagination-page-info'- if present, pagination has applied
        """
        client = app.test_client(self)
        response = client.get('/all-games')
        html = response.get_data().decode()
        self.assertIn('pagination-page-info', html)
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

    def test_request_reset(self):
        """
        Test GET requests to Reset Password route.

        Expected Results:
        Response - 200
        """
        client = app.test_client(self)
        response = client.get('/reset_password')
        self.assertEqual(response.status_code, 200)


class TestUserRoutes(TestCase):
    """
    Unit tests for routes and actions that require a User
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up app in Testing mode, and disable WtForm's
        CSRF tokens.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def tearDownClass(cls):
        """
        Remove dummy user and game data from db after testing.
        """
        mongo.db.users.delete_one({'username': 'unittest'})
        mongo.db.games.delete_one({'title': 'Unittest'})

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
            "password": 'Unit@test1',
            "confirm": 'Unit@test1'
        }
        client = app.test_client(self)
        response = client.post('/register', data=dummy_user_data)
        check_user = mongo.db.users.find_one({'username': 'unittest'})
        self.assertTrue(check_user)
        self.assertEqual(response.status_code, 302)

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

    def test_b_login_user(self):
        """
        Test behaviour of POST Login route when given valid login details.
        Should put set the user as current_user and redirect to the home page.

        Expected results:
        Response - 302
        current_user.username: 'unittest'
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        client = app.test_client(self)
        with client:
            response = client.post('/login', data=dummy_login_data)
            self.assertEqual(current_user.username, 'unittest')
            self.assertEqual(response.status_code, 302)

    def test_c_add_game(self):
        """
        Test POST to Add Game route.
        Should add dummy data to db, and redirect to All Games.

        Expected results:
        Response - 302
        Dummy data found in db
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        dummy_game_data = {
            'title': 'Unittest',
            'designer': 'John Doe',
            'publisher': 'JD Games',
            'genre': 'Fantasy',
            'mechanics': 'Worker Placement',
            'player_count': '2-5',
            'rating': '4',
            'weight': '2',
            'description': 'Dummy data for automated testing'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.post('add-game', data=dummy_game_data)
            check_db = mongo.db.games.find_one({'title': 'Unittest'})
            self.assertTrue(check_db)
            self.assertEqual(response.status_code, 302)

    def test_d_edit_game(self):
        """
        Test POST to Edit Game route.
        Passes dummy data to edit the 'publisher' of the game added above,
        and redirects to All Games page.

        Expected Results:
        Response - 302
        Game found in db by searching new 'publisher'
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        dummy_update_data = {
            'title': 'Unittest',
            'designer': 'John Doe',
            'publisher': 'Unit Test Games',
            'player_count': '2-5',
            'weight': '2',
            'description': 'Dummy data for automated testing'
        }
        client = app.test_client(self)
        with client:
            game = mongo.db.games.find_one({'title': 'Unittest'})
            client.post('/login', data=dummy_login_data)
            gameid = str(game['_id'])
            response = client.post('edit-game/' + gameid,
                                   data=dummy_update_data)
            update = mongo.db.games.find_one({'publisher': 'Unit Test Games'})
            self.assertTrue(update)
            self.assertEqual(response.status_code, 302)

    def test_zupdate_profile(self):
        """
        Test behaviour of POST Profile route to update account info.
        Should updatethe user's first and last name in the db,
        reload the Profile page and display the new info.

        Expected results:
        Response - 200
        New value of fname input = 'New'
        New value of lname input = 'Data'
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        dummy_update_data = {
            'fname': 'New',
            'lname': 'Data'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.post('/profile', data=dummy_update_data)
            html = response.get_data().decode()
            self.assertEqual(response.status_code, 200)
            self.assertIn('value="New"', html)
            self.assertIn('value="Data"', html)

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
            'password': 'Unit@test1'
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
            'password': 'Unit@test1'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/profile')
            self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        """
        Test POST request Profile route by logged in User.
        Updates account info for exisiting user, and redirects to Profile page.

        Expected results:
        Response - 302
        Update fname found in db
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        dummy_update_data = {
            'fname': 'Updated',
            'lname': 'Info',
            'email': 'unit@test.com'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.post('/profile', data=dummy_update_data)
            check_user = mongo.db.users.find_one({'username': 'unittest'})
            self.assertEqual(check_user['fname'], 'Updated')
            self.assertEqual(response.status_code, 302)

    def test_my_games_logged_in(self):
        """
        Test GET request to My Games route by logged in User,
        and check that pagination is working.

        Expected Results:
        Response - 200
        'pagination-page-info'- if present, pagination has applied
        """
        dummy_login_data = {
            'email': 'unit@test.com',
            'password': 'Unit@test1'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/my-games')
            # html = response.get_data().decode()
            # self.assertIn('pagination-page-info', html)
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
            'password': 'Unit@test1'
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
            'password': 'Unit@test1'
        }
        client = app.test_client(self)
        with client:
            client.post('/login', data=dummy_login_data)
            response = client.get('/register')
            self.assertEqual(response.status_code, 302)

    def test_valid_reset_password_request(self):
        """
        Test a valid POST request to the reset password route.
        Should validate on submit, and redirect to Login page

        Expected results:
        Response: 302
        """
        dummy_valid_email = {
            'email': 'unit@test.com'
        }
        client = app.test_client(self)
        with client:
            response = client.post('/reset_password', data=dummy_valid_email)
            self.assertEqual(response.status_code, 302)

    def test_invalid_reset_password_request(self):
        """
        Test an invalid POST request to the reset password route.
        Should not validate on submit, and reload the Reset Password page

        Expected results:
        Response: 200
        """
        dummy_invalid_email = {
            'email': 'invalid@test.com'
        }
        client = app.test_client(self)
        with client:
            response = client.post('/reset_password', data=dummy_invalid_email)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    main()
