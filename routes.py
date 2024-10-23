from flask import Blueprint, request, redirect, url_for, render_template
from models import db, Order, OrderItem, MenuItem, MenuItemCategory

# Define a blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Welcome to the Order Management System!"

@main.route('/add_order', methods=['GET', 'POST'])
def add_order():
    menu_items = MenuItem.query.all()  # Get all available menu items
    if request.method == 'POST':
        order = Order()
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID before adding order items

        total_price = 0.0
        for menu_item_id, quantity in request.form.items():
            if menu_item_id.startswith('item_'):
                menu_item_id = int(menu_item_id.split('_')[1])
                quantity = int(quantity)
                if quantity > 0:
                    menu_item = MenuItem.query.get(menu_item_id)
                    order_item = OrderItem(order_id=order.id, menu_item_id=menu_item.id, quantity=quantity)
                    db.session.add(order_item)
                    total_price += menu_item.price * quantity

        order.total_price = total_price
        db.session.commit()
        return redirect(url_for('main.view_orders'))

    return render_template('add_order.html', menu_items=menu_items)

@main.route('/orders', methods=['GET', 'POST'])
def view_orders():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'id')  # Default sort by Order ID
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order ascending

    # Build query based on search
    query = Order.query
    if search_query:
        if search_query.isdigit():
            query = query.filter_by(id=int(search_query))
        else:
            query = query.join(OrderItem).join(MenuItem).filter(MenuItem.item_name.ilike(f'%{search_query}%'))

    # Handle sorting
    if sort_order == 'asc':
        query = query.order_by(db.asc(getattr(Order, sort_by)))
    else:
        query = query.order_by(db.desc(getattr(Order, sort_by)))

    orders = query.all()
    return render_template('orders.html', orders=orders, search_query=search_query, sort_by=sort_by, sort_order=sort_order)

@main.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    order_items = OrderItem.query.filter_by(order_id=id).all()
    all_menu_items = MenuItem.query.all()

    if request.method == 'POST':
        total_price = 0.0
        for order_item in order_items:
            new_quantity = int(request.form.get(f'quantity_{order_item.id}', 0))
            if new_quantity > 0:
                order_item.quantity = new_quantity
                total_price += order_item.menu_item.price * new_quantity
            else:
                db.session.delete(order_item)

        for menu_item in all_menu_items:
            new_quantity = int(request.form.get(f'new_quantity_{menu_item.id}', 0))
            if new_quantity > 0:
                existing_order_item = OrderItem.query.filter_by(order_id=order.id, menu_item_id=menu_item.id).first()
                if not existing_order_item:
                    new_order_item = OrderItem(order_id=order.id, menu_item_id=menu_item.id, quantity=new_quantity)
                    db.session.add(new_order_item)
                total_price += menu_item.price * new_quantity

        order.total_price = total_price
        db.session.commit()
        return redirect(url_for('main.view_orders'))

    return render_template('edit_order.html', order=order, order_items=order_items, menu_items=all_menu_items)

@main.route('/complete_order/<int:id>')
def complete_order(id):
    order = Order.query.get_or_404(id)
    if order.status == 'active':
        order.status = 'completed'
        db.session.commit()
    return redirect(url_for('main.view_orders'))

@main.route('/delete_order/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('main.view_orders'))

@main.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        category = MenuItemCategory(category_name=category_name, description=description)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.view_categories'))
    return render_template('add_category.html')

@main.route('/categories', methods=['GET', 'POST'])
def view_categories():
    search_query = request.args.get('search', '')  # Get the search query from the input

    query = MenuItemCategory.query

    # Filter by search query (Category Name or Description)
    if search_query:
        query = query.filter(
            MenuItemCategory.category_name.ilike(f'%{search_query}%') |
            MenuItemCategory.description.ilike(f'%{search_query}%')
        )

    categories = query.all()

    return render_template('categories.html', categories=categories, search_query=search_query)

@main.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    categories = MenuItemCategory.query.all()
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        menu_item = MenuItem(item_name=item_name, description=description, price=price, category_id=category_id)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('main.view_menu_items'))
    return render_template('add_menu_item.html', categories=categories)

@main.route('/menu_items', methods=['GET', 'POST'])
def view_menu_items():
    search_query = request.args.get('search', '')  # Get search query from input
    category_filter = request.args.get('category_filter', '')  # Get category filter from input

    query = MenuItem.query

    # Filter by search query (Menu Item name)
    if search_query:
        query = query.filter(MenuItem.item_name.ilike(f'%{search_query}%'))

    # Filter by category if a filter is selected
    if category_filter:
        query = query.filter_by(category_id=category_filter)

    menu_items = query.all()
    categories = MenuItemCategory.query.all()  # To populate the category filter dropdown

    return render_template('menu_items.html', menu_items=menu_items, search_query=search_query, category_filter=category_filter, categories=categories)