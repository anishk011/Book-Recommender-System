#!/usr/bin/env python3
"""
Simple startup script for the Book Recommender application
"""

import os
import sys
from app import create_app

def main():
    """Main function to run the application"""
    try:
        # Get environment from environment variable or default to development
        env = os.getenv('FLASK_ENV', 'development')
        
        # Create the application
        app = create_app(env)
        
        # Get port from environment variable or default to 5000
        port = int(os.environ.get('PORT', 5000))
        
        print(f"🚀 Starting Book Recommender in {env} mode...")
        print(f"📖 Application will be available at: http://localhost:{port}")
        print(f"🔧 Environment: {env}")
        print(f"🐛 Debug mode: {app.config['DEBUG']}")
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=port,
            debug=app.config['DEBUG']
        )
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
