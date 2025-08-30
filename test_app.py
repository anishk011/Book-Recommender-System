import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBookRecommender(unittest.TestCase):
    """Test cases for the Book Recommender application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = None
    
    @patch('models.book_recommender.BookRecommender')
    def test_app_creation(self, mock_recommender):
        """Test that the Flask app can be created successfully"""
        from app import create_app
        
        # Mock the recommender to avoid loading actual model files
        mock_recommender_instance = MagicMock()
        mock_recommender.return_value = mock_recommender_instance
        
        try:
            app = create_app('testing')
            self.assertIsNotNone(app)
            self.assertEqual(app.config['TESTING'], True)
        except Exception as e:
            self.fail(f"App creation failed: {e}")
    
    def test_config_loading(self):
        """Test configuration loading"""
        from config import config
        
        self.assertIn('development', config)
        self.assertIn('production', config)
        self.assertIn('testing', config)
        self.assertIn('default', config)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        from app import create_app
        
        with patch('models.book_recommender.BookRecommender') as mock_recommender:
            mock_recommender_instance = MagicMock()
            mock_recommender.return_value = mock_recommender_instance
            
            app = create_app('testing')
            
            with app.test_client() as client:
                response = client.get('/health')
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIn('status', data)

if __name__ == '__main__':
    unittest.main()
