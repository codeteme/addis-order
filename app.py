from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main  # Import the routes blueprint

# Initialize Flask app
app = Flask(__name__)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tmt0947:password@localhost/addis_order_db'
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