##  Addis Order - Restaurant Management System

Addis Order is a restaurant management system designed for businesses specializing in meat-based menus. The system streamlines order management, inventory tracking, and communication between waitstaff, butchers, and kitchen staff.

### Features

* Order Management:
	* Add, view, edit, and delete orders.
	* Track order statuses (active or completed).
	* Automatically calculate order totals based on menu items and quantities.
* Menu Management:
	* Add, view, edit, and delete menu items.
	* Organize menu items by categories.
	* Set prices and descriptions for menu items.
* Inventory Management:
	* Add, view, edit, and delete inventory items.
	* Track stock quantities, reorder levels, and optional expiration dates.
	* Categorize inventory items and associate them with suppliers.
* Search and Filter:
	* Search orders by Order ID or menu item names.
	* Filter orders by status.
	* Search and filter menu items and categories.
* User-Friendly Interface:
	* Navigation links for orders, menu items, and categories.
	* Dynamic table sorting by columns.
	* Modern, responsive design.

### Technologies Used

* Backend: Flask (Python)
* Frontend: Jinja2 templates, Bootstrap 5
* Database: PostgreSQL
* Environment Management: dotenv
* Deployment: Render and Docker with Gunicorn

### Setup Instructions

#### Prerequisites

* Python 3.11 or higher
* PostgreSQL
* pipenv or virtualenv
* Docker (optional for deployment)

#### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/addis-order.git
cd addis-order
```

2. Set up a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up the database:
	* Create a PostgreSQL database (e.g., addis_order_db).
	* Update .env.development with your database credentials.

5.	Run migrations:
```
flask db upgrade
```

6. Start the development server:
```
flask run
```
### Deployment

#### Using Docker

1.	Build the Docker image:
```
docker build -t addis-order .
```

2.	Run the container:
```
docker run -p 8000:8000 addis-order
```


Using Render

	1.	Deploy the application and PostgreSQL database to Render.
	2.	Set the following environment variables in Render:
	•	DB_USER
	•	DB_PASSWORD
	•	DB_HOST
	•	DB_PORT
	•	DB_NAME
	•	SECRET_KEY
	•	ENV=production
	•	FLASK_ENV=production

Configuration

Environment Variables

	•	Development environment: .env.development
	•	Production environment: Environment variables are loaded directly.

Example .env.development:

```
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=addis_order_db
SECRET_KEY=your-secret-key
ENV=development
FLASK_ENV=development
```

### Testing

1. Run the Flask app in development mode:

```
flask run
```

2. Test features like adding, editing, and deleting orders, menu items, and inventory.

### Contributing

Feel free to submit issues or pull requests for improvements. Contributions are welcome!

### License

This project is licensed under the MIT License.