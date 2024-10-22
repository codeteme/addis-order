from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    status = db.Column(db.String(10), nullable=False, default='active')  # Status column

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