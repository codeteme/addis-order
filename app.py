from flask import Flask, request, redirect, url_for, render_template
from flask_migrate import Migrate
from models import db, Order  # Import from models.py

# Initialize Flask app
app = Flask(__name__)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tmt0947:password@localhost/addis_order_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Create the tables in the database
with app.app_context():
    db.create_all()

# Route to display the home page
@app.route('/')
def index():
    return "Welcome to the Order Management System!"

# Route to add a new order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        order = Order(item=item, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('view_orders'))
    return render_template('add_order.html')

# Route to view all orders
@app.route('/orders')
def view_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

# Route to edit an order
@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    if request.method == 'POST':
        order.item = request.form.get('item')
        order.quantity = request.form.get('quantity')
        db.session.commit()
        return redirect(url_for('view_orders'))
    return render_template('edit_order.html', order=order)

# Route to mark an order as completed
@app.route('/complete_order/<int:id>')
def complete_order(id):
    order = Order.query.get_or_404(id)
    if order.status == 'active':
        order.status = 'completed'
        db.session.commit()
    return redirect(url_for('view_orders'))

# Route to delete an order
@app.route('/delete_order/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('view_orders'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)