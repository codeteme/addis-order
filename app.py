from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

orders = []

@app.route('/')
def index():
    return "Welcome to the Order Management System!"

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        # Create an order with unique ID
        order_id = len(orders) + 1
        order = {'id': order_id, 'item': item, 'quantity': quantity}
        orders.append(order)
        return redirect(url_for('view_orders'))
    return render_template('add_order.html')

@app.route('/orders')
def view_orders():
    return render_template('orders.html', orders=orders)

@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = next((o for o in orders if o['id'] == id), None)
    if order:
        if request.method == 'POST':
            # Update order details
            order['item'] = request.form.get('item')
            order['quantity'] = request.form.get('quantity')
            return redirect(url_for('view_orders'))
        return render_template('edit_order.html', order=order)
    return "Order not found", 404

@app.route('/delete_order/<int:id>')
def delete_order(id):
    global orders
    orders = [order for order in orders if order['id'] != id]
    return redirect(url_for('view_orders'))

if __name__ == '__main__':
    app.run(debug=True)