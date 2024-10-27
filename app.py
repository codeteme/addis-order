import os
from dotenv import load_dotenv  # Import dotenv to load environment variables
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main  # Import the routes blueprint

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Set the secret key to a random value or read it from an environment variable for security
app.config['SECRET_KEY'] = os.urandom(24)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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