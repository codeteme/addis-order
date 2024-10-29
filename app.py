import os
from dotenv import load_dotenv  # Import dotenv to load environment variables
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main  # Import the routes blueprint

print("Loading environment variables from .env file.")
load_dotenv()  # Load environment variables from .env file

# Initialize Flask app
app = Flask(__name__)

print("Test")
print(f"Current working directory: {os.getcwd()}")
print(f"Environment variables: {os.environ}")

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Manual Test: dev")
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Manual Test: prod")
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

print("Works")
# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register the blueprint
app.register_blueprint(main)

# Create the tables in the database
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)