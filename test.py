from aboveboard import app
from unittest import TestCase, main


class FirstTestCase(TestCase):

    def test_index(self):
        client = app.test_client(self)
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    main()
