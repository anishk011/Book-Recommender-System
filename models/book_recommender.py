import pickle
import os
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BookRecommender:
    """Book recommendation system using collaborative filtering"""
    
    def __init__(self, model_path: str = './'):
        """
        Initialize the book recommender with pre-trained models
        
        Args:
            model_path: Path to the directory containing model files
        """
        self.model_path = model_path
        self.popular_df = None
        self.pt = None
        self.books = None
        self.similarity_scores = None
        self._load_models()
    
    def _load_models(self):
        """Load all pre-trained models and data"""
        try:
            # Check if all required files exist
            required_files = ['popular.pkl', 'pt.pkl', 'books.pkl', 'similarity_scores.pkl']
            missing_files = []
            
            for file in required_files:
                file_path = os.path.join(self.model_path, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            
            if missing_files:
                logger.warning(f"Missing model files: {missing_files}. Creating empty models.")
                self._create_empty_models()
                return
            
            # Load all models
            self.popular_df = pickle.load(open(f'{self.model_path}popular.pkl', 'rb'))
            self.pt = pickle.load(open(f'{self.model_path}pt.pkl', 'rb'))
            self.books = pickle.load(open(f'{self.model_path}books.pkl', 'rb'))
            self.similarity_scores = pickle.load(open(f'{self.model_path}similarity_scores.pkl', 'rb'))
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            logger.info("Creating empty models as fallback")
            self._create_empty_models()
    
    def _create_empty_models(self):
        """Create empty models for development/testing when real models are not available"""
        import pandas as pd
        
        # Create empty DataFrames
        self.popular_df = pd.DataFrame(columns=['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating'])
        self.pt = pd.DataFrame()
        self.books = pd.DataFrame(columns=['Book-Title', 'Book-Author', 'Image-URL-M'])
        self.similarity_scores = np.array([])
        
        logger.info("Empty models created for development/testing")
    
    def get_popular_books(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get the most popular books
        
        Args:
            limit: Number of books to return
            
        Returns:
            List of popular books with their details
        """
        try:
            popular_books = []
            for i in range(min(limit, len(self.popular_df))):
                book = {
                    'title': self.popular_df.iloc[i]['Book-Title'],
                    'author': self.popular_df.iloc[i]['Book-Author'],
                    'image_url': self.popular_df.iloc[i]['Image-URL-M'],
                    'votes': int(self.popular_df.iloc[i]['num_ratings']),
                    'rating': float(self.popular_df.iloc[i]['avg_rating'])
                }
                popular_books.append(book)
            return popular_books
        except Exception as e:
            logger.error(f"Error getting popular books: {e}")
            return []
    
    def get_book_recommendations(self, book_title: str, num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Get book recommendations based on a given book title
        
        Args:
            book_title: Title of the book to find recommendations for
            num_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended books with their details
        """
        try:
            # Find the index of the book in the pivot table
            if book_title not in self.pt.index:
                logger.warning(f"Book '{book_title}' not found in the dataset")
                return []
            
            book_index = np.where(self.pt.index == book_title)[0][0]
            
            # Get similar books based on similarity scores
            similar_items = sorted(
                list(enumerate(self.similarity_scores[book_index])),
                key=lambda x: x[1],
                reverse=True
            )[1:num_recommendations + 1]
            
            recommendations = []
            for item in similar_items:
                similar_book_title = self.pt.index[item[0]]
                temp_df = self.books[self.books['Book-Title'] == similar_book_title]
                
                if not temp_df.empty:
                    book_data = temp_df.drop_duplicates('Book-Title').iloc[0]
                    recommendation = {
                        'title': book_data['Book-Title'],
                        'author': book_data['Book-Author'],
                        'image_url': book_data['Image-URL-M'],
                        'similarity_score': float(item[1])
                    }
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations for '{book_title}': {e}")
            return []
    
    def search_books(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for books by title or author
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching books
        """
        try:
            query = query.lower()
            matching_books = []
            
            # Search in popular books first
            for _, book in self.popular_df.iterrows():
                if (query in book['Book-Title'].lower() or 
                    query in book['Book-Author'].lower()):
                    matching_books.append({
                        'title': book['Book-Title'],
                        'author': book['Book-Author'],
                        'image_url': book['Image-URL-M'],
                        'votes': int(book['num_ratings']),
                        'rating': float(book['avg_rating'])
                    })
                    
                    if len(matching_books) >= limit:
                        break
            
            return matching_books
            
        except Exception as e:
            logger.error(f"Error searching books: {e}")
            return []
    
    def get_available_books(self) -> List[str]:
        """
        Get list of all available book titles for autocomplete
        
        Returns:
            List of book titles
        """
        try:
            return list(self.pt.index)
        except Exception as e:
            logger.error(f"Error getting available books: {e}")
            return []
