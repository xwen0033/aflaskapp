import unittest
from src.app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home_endpoint(self):
        # Test the / endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

if __name__ == '__main__':
    unittest.main()