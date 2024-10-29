import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main  # Import your blueprint here


# Initialize Flask app
app = Flask(__name__)

# Check the environment and load the appropriate .env file
if 'WEBSITE_HOSTNAME' in os.environ:
    # Load production settings
    print("production")
    ENV="production"
    FLASK_ENV="production"

    # Database connection parameters
    DB_USER=os.environ.get('DB_USER')
    DB_PASSWORD=os.environ.get('DB_PASSWORD')
    DB_HOST=os.environ.get('DB_HOST')
    DB_PORT=os.environ.get('DB_PORT')
    DB_NAME=os.environ.get('DB_NAME')

    print("+++++++++++++++++++++")
    print(DB_USER)
    print(DB_PASSWORD)
    print(DB_HOST)
    print(DB_PORT)
    print(DB_NAME)

    print("+++++++++++++++++++++")
    print(os.getenv('DB_USER'))
    print(os.getenv('DB_PASSWORD'))
    print(os.getenv('DB_HOST'))
    print(os.getenv('DB_PORT'))
    print(os.getenv('DB_NAME'))
    
    app.config['ENV'] = ENV
    app.config['FLASK_ENV'] = FLASK_ENV

else:
    # Load development settings
    print("development")
    load_dotenv('.env.development')


# Set up database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
    app.run(debug=True)