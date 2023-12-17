import unittest
from src.app import app
from unittest.mock import patch, MagicMock


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home_endpoint_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        assert b'Data Analyzer' in response.data

    @patch('src.routes.analyze_folder_word_count')
    def test_home_endpoint_post(self, mock_analyse):
        mock_analyse.return_value = "Mock Data"
        post_data = {'folder_path': 'test_folder'}
        with patch(
                "src.routes.plot_word_count",
                return_value='test_plot'
        ) as mock_plot:
            response = self.app.post('/', data=post_data, follow_redirects=True)
            mock_plot.assert_called_once_with("Mock Data")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test_plot', response.data)

    def test_seasonality_endpoint_get(self):
        response = self.app.get('/seasonality')
        self.assertEqual(response.status_code, 200)
        assert b'Enter the data path' in response.data

    @patch('src.routes.read_csv_from_path')
    def test_seasonality_endpoint_post(self, mock_read):
        mock_data = MagicMock(empty=False)
        mock_read.return_value = mock_data
        post_data = {'data_path': 'mock.csv'}
        with patch(
                "src.routes.data_preparation",
                return_value=('mock data A', 'mock data B')
        ) as mock_data_prep, patch(
            "src.routes.plot_temp",
            return_value='test_plot'
        ) as mock_plot:
            response = self.app.post('/seasonality', data=post_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            mock_data_prep.assert_called_once_with(mock_data)
            mock_plot.assert_called_once_with('mock data A', 'mock data B')
