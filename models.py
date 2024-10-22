from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    status = db.Column(db.String(10), nullable=False, default='active')
    total_price = db.Column(db.Float, nullable=False, default=0.0)  # Automatically calculated

    def __repr__(self):
        return f'<Order {self.item} - {self.status}>'

class MenuItemCategory(db.Model):
    __tablename__ = 'menu_item_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # Relationship to MenuItems (one category can have many items)
    menu_items = db.relationship('MenuItem', backref='category', lazy=True)

    def __repr__(self):
        return f'<MenuItemCategory {self.category_name}>'

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_item_categories.id'), nullable=False)  # Foreign key to category

    def __repr__(self):
        return f'<MenuItem {self.item_name}>'
    
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Relationships
    menu_item = db.relationship('MenuItem', backref='order_items')
    order = db.relationship('Order', backref='order_items')