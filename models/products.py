from models.database import db
from sqlalchemy.orm import validates

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))    # Store image file path
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='products')

    def __init__(self, name, price, image, description, category_id):
        self.name = name
        self.price = price
        self.image = image
        self.description = description
        self.category_id = category_id

    @validates('price')
    def validate_positive_number(self, key, value):
        if value < 1:
            raise ValueError(f"{key} must be a positive integer")
        return value
    def __repr__(self):
        return f"<Product {self.name} {self.image}>"


# Define Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    products = db.relationship('Product', back_populates='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Category {self.name}>"
