import unittest
from src.app import app
from unittest.mock import patch, MagicMock

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home_endpoint_get(self):
        # Test the / endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        assert b'Data Analyzer' in response.data

    @patch('src.routes.analyze_folder_word_count')
    def test_home_endpoint_post(self, mock_analyse):
        mock_analyse.return_value = "Mocked Data"
        post_data = {'folder_path': 'test_folder'}
        with patch(
            "src.routes.plot_word_count",
            return_value='test_plot'
        ) as mock_plot:
            response = self.app.post('/', data=post_data, follow_redirects=True)
            mock_plot.assert_called_once_with("Mocked Data")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test_plot', response.data)

