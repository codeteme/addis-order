import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main

# Initialize Flask app
app = Flask(__name__)

# Check the environment and load the appropriate .env file
if 'WEBSITE_HOSTNAME' in os.environ:
    # Production environment
    print("Loading production environment variables...")
    
    # Print each environment variable with descriptive labels for debugging
    print("Production Environment Variables:")
    print("DB_USER:", os.environ.get('DB_USER'))
    print("DB_PASSWORD:", os.environ.get('DB_PASSWORD'))
    print("DB_HOST:", os.environ.get('DB_HOST'))
    print("DB_PORT:", os.environ.get('DB_PORT'))
    print("DB_NAME:", os.environ.get('DB_NAME'))
    print("SECRET_KEY:", os.environ.get('SECRET_KEY'))
    print("ENV:", os.environ.get('ENV'))
    print("FLASK_ENV:", os.environ.get('FLASK_ENV'))
    
    # Configure the database URI with SSL required for production
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"
    )
    
    # Set other production environment configurations
    app.config['ENV'] = 'production'
    app.config['FLASK_ENV'] = 'production'

else:
    # Development environment
    print("Loading development environment variables...")
    load_dotenv('.env.development')

    # Print each environment variable with descriptive labels for debugging
    print("Development Environment Variables:")
    print("DB_USER:", os.getenv('DB_USER'))
    print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
    print("DB_HOST:", os.getenv('DB_HOST'))
    print("DB_PORT:", os.getenv('DB_PORT'))
    print("DB_NAME:", os.getenv('DB_NAME'))
    print("SECRET_KEY:", os.getenv('SECRET_KEY'))
    print("ENV:", os.getenv('ENV'))
    print("FLASK_ENV:", os.getenv('FLASK_ENV'))

    # Configure the database URI for development (no SSL required)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

# Common configurations
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Debug output for SQLALCHEMY_DATABASE_URI and configurations (remove in production)
print("+++++++++++++++++++++")
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
print("Environment:", app.config['ENV'])
print("Secret Key:", app.config['SECRET_KEY'])
print("+++++++++++++++++++++")

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register the blueprint
app.register_blueprint(main)

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    # Set debug mode based on environment
    app.run(debug=(app.config['FLASK_ENV'] == 'development'))