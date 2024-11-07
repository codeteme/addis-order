Here’s an updated version of your README file to reflect the changes, including the Docker setup and Gunicorn configuration:

AddisOrder

AddisOrder is an intuitive restaurant order management system designed specifically for the vibrant dining scene in Ethiopia. This platform streamlines order processing, enhances communication between waitstaff and kitchens, and simplifies inventory management.

Project Setup

1. Clone the Repository

Clone the repo to your local machine:

git clone https://github.com/codeteme/addis-order.git
cd addis-order

2. Environment Variables

The application uses environment variables for configuration, managed by .env files.
	•	Development: Configure .env.development with the following variables:

# Database connection parameters
DB_USER=postgres
DB_PASSWORD=password  # Replace with actual password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=addis_order_db

# Flask environment configuration
ENV=development
FLASK_APP=app.py
FLASK_ENV=development

# Secret Key for session management
SECRET_KEY=your_secret_key_here


	•	Production: Set these variables in your production environment (e.g., on Azure) to ensure the application connects to the correct database and has the correct secret key.

3. Install Dependencies

Create a virtual environment and install the dependencies:

python -m venv venv
source venv/bin/activate  # For Windows, use venv\Scripts\activate
pip install -r requirements.txt

4. Database Migration

Ensure your database is ready by running migrations:

flask db upgrade

This will set up the necessary database tables.

Running the Application

Development Mode

To run the application in development mode with flask run, use:

flask run

This command starts the application in debug mode, which auto-reloads on code changes and shows detailed error messages.

Production Mode with Gunicorn

For production, use Gunicorn to serve the application:

gunicorn --workers 4 --bind 0.0.0.0:8000 app:app

This command starts the application with 4 worker processes, listening on port 8000.

Docker Setup

The project includes a Dockerfile for containerized deployment.
	1.	Build the Docker Image:

docker build -t addisorder .


	2.	Run the Docker Container:

docker run -p 8000:8000 addisorder



This starts the containerized application on port 8000. The app is served by Gunicorn inside the Docker container, as specified in the CMD instruction of the Dockerfile.

Configuration Files

Gunicorn Configuration

A custom gunicorn.conf.py file is provided to configure Gunicorn for optimal performance in production. Key settings include:
	•	Worker Processes: The number of worker processes is calculated as cpu_count * 2 + 1.
	•	Binding: The application is set to bind to 0.0.0.0:8000, making it accessible on port 8000.

Dockerfile

The Dockerfile is set up to:
	1.	Use the python:3.11-slim base image.
	2.	Install necessary dependencies (libpq-dev and gcc for PostgreSQL).
	3.	Copy project files and install Python packages.
	4.	Start the application using Gunicorn.

Collaboration Guide

Development Workflow

	1.	Create a new branch for your work:

git checkout -b feature-branch


	2.	Make your changes, then stage and commit:

git add .
git commit -m "Your descriptive commit message"


	3.	Push the branch and create a pull request:

git push origin feature-branch


	4.	Open a pull request on GitHub and request a review.

Keeping Your Branch Updated

	1.	Pull the latest changes from main:

git checkout main
git pull origin main


	2.	Rebase your feature branch:

git checkout feature-branch
git rebase main


	3.	Resolve conflicts if necessary, then push your updated branch.

License

This project is licensed under the MIT License. See the LICENSE file for details.

This README should cover all necessary steps for setting up, running, and collaborating on the project, including both Docker and Gunicorn configurations. Let me know if there’s anything specific you’d like added!