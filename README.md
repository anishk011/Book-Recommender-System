# Book Recommender System

A modern, intelligent book recommendation system built with Flask and machine learning. Discover your next favorite book with our collaborative filtering algorithm.

## 🌟 Features

- **Smart Recommendations**: Get personalized book recommendations based on collaborative filtering
- **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5 and modern animations
- **Autocomplete Search**: Intelligent search with real-time book suggestions
- **Popular Books**: Browse the most popular and highly-rated books
- **API Endpoints**: RESTful API for integration with other applications
- **Error Handling**: Comprehensive error handling and user-friendly error pages
- **Mobile Responsive**: Works perfectly on all devices and screen sizes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bookRecommender
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your configuration
   # SECRET_KEY=your-secret-key-here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
bookRecommender/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
├── runtime.txt          # Python runtime version
├── README.md           # Project documentation
├── models/
│   ├── __init__.py
│   └── book_recommender.py  # ML recommendation logic
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── recommend.html      # Recommendations page
│   └── errors/
│       ├── 404.html        # 404 error page
│       ├── 500.html        # 500 error page
│       └── error.html      # Generic error page
└── model/                  # ML model files (not in repo)
    ├── popular.pkl
    ├── pt.pkl
    ├── books.pkl
    └── similarity_scores.pkl
```

## 🔧 Configuration

The application uses environment variables for configuration:

- `FLASK_ENV`: Environment mode (development/production)
- `SECRET_KEY`: Flask secret key for session management
- `DEBUG`: Enable/disable debug mode
- `MODEL_PATH`: Path to ML model files

## 🎯 API Endpoints

### Web Pages
- `GET /` - Home page with popular books
- `GET /recommend` - Book recommendation page
- `POST /recommend_books` - Get book recommendations

### API Endpoints
- `GET /api/books/popular` - Get popular books (JSON)
- `GET /api/books/recommendations?book=<title>` - Get recommendations (JSON)
- `GET /search?q=<query>` - Search books (JSON)
- `GET /health` - Health check endpoint

## 🚀 Deployment

### Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set FLASK_ENV=production
   ```

### Render

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure the service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: Set `SECRET_KEY` and `FLASK_ENV=production`

### Vercel

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

## 🛠️ Development

### Running Tests
```bash
# Set testing environment
export FLASK_ENV=testing

# Run the application in test mode
python app.py
```

### Code Style
The project follows PEP 8 style guidelines. Use a linter like `flake8` or `black` for code formatting.

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test thoroughly
3. Commit changes: `git commit -m "Add new feature"`
4. Push and create pull request

## 🔒 Security

- Input validation and sanitization
- CSRF protection
- Secure headers
- Environment-based configuration
- Error handling without exposing sensitive information

## 📊 Performance

- Optimized database queries
- Caching for frequently accessed data
- Efficient ML model loading
- Responsive image loading with fallbacks
- Minified CSS and JavaScript

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the error logs
2. Verify your environment configuration
3. Ensure all dependencies are installed
4. Check that model files are in the correct location

For additional support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for the beautiful UI components
- Font Awesome for icons
- The machine learning community for collaborative filtering algorithms

---

**Made with ❤️ for book lovers everywhere**
