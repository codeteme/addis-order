from flask import Flask, request, redirect, url_for, render_template
from flask_migrate import Migrate
from models import db, Order, OrderItem, MenuItem, MenuItemCategory  # Import models

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

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    menu_items = MenuItem.query.all()  # Get all available menu items

    if request.method == 'POST':
        order = Order()
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID before adding order items

        total_price = 0.0

        # Loop through the submitted menu items and quantities
        for menu_item_id, quantity in request.form.items():
            if menu_item_id.startswith('item_'):  # Filter for menu item entries
                menu_item_id = int(menu_item_id.split('_')[1])  # Extract ID
                quantity = int(quantity)

                if quantity > 0:
                    menu_item = MenuItem.query.get(menu_item_id)
                    order_item = OrderItem(order_id=order.id, menu_item_id=menu_item.id, quantity=quantity)
                    db.session.add(order_item)

                    # Update total price
                    total_price += menu_item.price * quantity

        # Update the order with the calculated total price
        order.total_price = total_price
        db.session.commit()

        return redirect(url_for('view_orders'))

    return render_template('add_order.html', menu_items=menu_items)

# Route to view all orders
@app.route('/orders')
def view_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

# Route to edit an order
@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)  # Get the order by ID
    order_items = OrderItem.query.filter_by(order_id=id).all()  # Get the associated order items
    all_menu_items = MenuItem.query.all()  # Get all available menu items
    
    if request.method == 'POST':
        total_price = 0.0

        # Update existing order items
        for order_item in order_items:
            new_quantity = int(request.form.get(f'quantity_{order_item.id}', 0))
            
            # Update quantity if it's greater than zero
            if new_quantity > 0:
                order_item.quantity = new_quantity
                total_price += order_item.menu_item.price * new_quantity
            else:
                # If quantity is zero, delete the order item
                db.session.delete(order_item)

        # Add new items to the order
        for menu_item in all_menu_items:
            new_quantity = int(request.form.get(f'new_quantity_{menu_item.id}', 0))
            if new_quantity > 0:
                # Check if this menu item is already in the order
                existing_order_item = OrderItem.query.filter_by(order_id=order.id, menu_item_id=menu_item.id).first()
                if not existing_order_item:
                    # Add the new item to the order
                    new_order_item = OrderItem(order_id=order.id, menu_item_id=menu_item.id, quantity=new_quantity)
                    db.session.add(new_order_item)
                total_price += menu_item.price * new_quantity

        # Update the total price of the order
        order.total_price = total_price
        db.session.commit()

        return redirect(url_for('view_orders'))

    return render_template('edit_order.html', order=order, order_items=order_items, menu_items=all_menu_items)

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


# Route to add a new category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        category = MenuItemCategory(category_name=category_name, description=description)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('view_categories'))
    return render_template('add_category.html')

# Route to view all categories
@app.route('/categories')
def view_categories():
    categories = MenuItemCategory.query.all()
    return render_template('categories.html', categories=categories)

# Route to add a new menu item
@app.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    categories = MenuItemCategory.query.all()  # Get all categories for the dropdown
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        category_id = request.form.get('category_id')  # Get selected category
        menu_item = MenuItem(item_name=item_name, description=description, price=price, category_id=category_id)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('view_menu_items'))
    return render_template('add_menu_item.html', categories=categories)

# Route to view all menu items
@app.route('/menu_items')
def view_menu_items():
    menu_items = MenuItem.query.all()
    return render_template('menu_items.html', menu_items=menu_items)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)