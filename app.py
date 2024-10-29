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

# Environment and directory diagnostics
print("Environment diagnostics:")
print(f"Current working directory: {os.getcwd()}")
print(f"Environment variables loaded: {list(os.environ.keys())}")

# Determine environment (production vs. development)
if 'WEBSITE_HOSTNAME' not in os.environ:
    # Local development environment
    print("Environment: Development")
    print("Loading development configuration.")
    app.config.from_object('azureproject.development')
else:
    # Production environment
    print("Environment: Production")
    print("Loading production configuration.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

print("Database configuration complete.")

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register the blueprint
app.register_blueprint(main)

# Create tables if not exist
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask app on port {port}...")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=(app.config['ENV'] == 'development')
    )