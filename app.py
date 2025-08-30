import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import traceback

from config import config
from models.book_recommender import BookRecommender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize book recommender
    try:
        recommender = BookRecommender()
        app.recommender = recommender
        logger.info("Book recommender initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize book recommender: {e}")
        app.recommender = None
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register routes
    register_routes(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return render_template('errors/error.html', error=e), e.code

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def index():
        """Home page with popular books"""
        try:
            if app.recommender is None:
                flash('Book recommender system is currently unavailable', 'error')
                return render_template('index.html', books=[])
            
            books = app.recommender.get_popular_books(limit=50)
            return render_template('index.html', books=books)
        except Exception as e:
            logger.error(f"Error in index route: {e}")
            flash('An error occurred while loading popular books', 'error')
            return render_template('index.html', books=[])
    
    @app.route('/recommend')
    def recommend_page():
        """Recommendation page"""
        try:
            if app.recommender is None:
                flash('Book recommender system is currently unavailable', 'error')
                return render_template('recommend.html', recommendations=[])
            
            # Get available books for autocomplete
            available_books = app.recommender.get_available_books()
            return render_template('recommend.html', recommendations=[], available_books=available_books)
        except Exception as e:
            logger.error(f"Error in recommend page: {e}")
            flash('An error occurred while loading the recommendation page', 'error')
            return render_template('recommend.html', recommendations=[])
    
    @app.route('/recommend_books', methods=['POST'])
    def recommend_books():
        """Get book recommendations"""
        try:
            if app.recommender is None:
                flash('Book recommender system is currently unavailable', 'error')
                return redirect(url_for('recommend_page'))
            
            user_input = request.form.get('user_input', '').strip()
            
            if not user_input:
                flash('Please enter a book title', 'warning')
                return redirect(url_for('recommend_page'))
            
            # Get recommendations
            recommendations = app.recommender.get_book_recommendations(user_input, num_recommendations=5)
            
            if not recommendations:
                flash(f'No recommendations found for "{user_input}". Please try a different book title.', 'warning')
                return redirect(url_for('recommend_page'))
            
            # Get available books for autocomplete
            available_books = app.recommender.get_available_books()
            
            flash(f'Found {len(recommendations)} recommendations for "{user_input}"', 'success')
            return render_template('recommend.html', recommendations=recommendations, 
                                 search_query=user_input, available_books=available_books)
            
        except Exception as e:
            logger.error(f"Error in recommend_books: {e}")
            flash('An error occurred while getting recommendations', 'error')
            return redirect(url_for('recommend_page'))
    
    @app.route('/search')
    def search_books():
        """Search books API endpoint"""
        try:
            if app.recommender is None:
                return jsonify({'error': 'Book recommender system is currently unavailable'}), 503
            
            query = request.args.get('q', '').strip()
            
            if not query:
                return jsonify({'books': []})
            
            books = app.recommender.search_books(query, limit=10)
            return jsonify({'books': books})
            
        except Exception as e:
            logger.error(f"Error in search_books: {e}")
            return jsonify({'error': 'An error occurred while searching'}), 500
    
    @app.route('/api/books/popular')
    def api_popular_books():
        """API endpoint for popular books"""
        try:
            if app.recommender is None:
                return jsonify({'error': 'Book recommender system is currently unavailable'}), 503
            
            limit = request.args.get('limit', 20, type=int)
            books = app.recommender.get_popular_books(limit=limit)
            return jsonify({'books': books})
            
        except Exception as e:
            logger.error(f"Error in api_popular_books: {e}")
            return jsonify({'error': 'An error occurred while fetching popular books'}), 500
    
    @app.route('/api/books/recommendations')
    def api_recommendations():
        """API endpoint for book recommendations"""
        try:
            if app.recommender is None:
                return jsonify({'error': 'Book recommender system is currently unavailable'}), 503
            
            book_title = request.args.get('book', '').strip()
            limit = request.args.get('limit', 5, type=int)
            
            if not book_title:
                return jsonify({'error': 'Book title is required'}), 400
            
            recommendations = app.recommender.get_book_recommendations(book_title, num_recommendations=limit)
            return jsonify({'recommendations': recommendations})
            
        except Exception as e:
            logger.error(f"Error in api_recommendations: {e}")
            return jsonify({'error': 'An error occurred while getting recommendations'}), 500
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for deployment"""
        try:
            status = {
                'status': 'healthy',
                'recommender_available': app.recommender is not None
            }
            return jsonify(status)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# Create the application instance
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])




