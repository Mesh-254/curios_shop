from models.database import db
from models.stock import Stock
from datetime import datetime, timedelta
from sqlalchemy import DateTime
from sqlalchemy.orm import validates


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.String(12), unique=True)
    address = db.Column(db.String(200))
    email = db.Column(db.String(254), unique=True)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Supplier(id={self.id}, name={self.name}, phone={self.phone}, address={self.address}, email={self.email})"


class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
                            nullable=False)  # Foreign key referencing Supplier.id
    quantity = db.Column(db.Integer, default=1)
    perprice = db.Column(db.Integer, default=1)
    totalprice = db.Column(db.Integer, default=1)
    date = db.Column(DateTime, default=datetime.utcnow() + timedelta(hours=3))

    supplier = db.relationship('Supplier', backref='purchase_items')
    stock = db.relationship('Stock', backref='purchase_items')

    @validates('quantity', 'perprice', 'totalprice')
    def validate_positive_number(self, key, value):
        if value < 1:
            raise ValueError(f"{key} must be a positive integer")
        return value

    def __repr__(self):
        return f"PurchaseItem(id={self.id}, stock_id={self.stock_id}, quantity={self.quantity}, perprice={self.perprice}, totalprice={self.totalprice})"


class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    perprice = db.Column(db.Integer, default=1)
    totalprice = db.Column(db.Integer, default=1)
    date = db.Column(DateTime, default=datetime.utcnow() + timedelta(hours=3))

    stock = db.relationship('Stock', backref='sale_items')

    @validates('quantity', 'perprice', 'totalprice')
    def validate_positive_number(self, key, value):
        if value < 1:
            raise ValueError(f"{key} must be a positive integer")
        return value

    def __repr__(self):
        return f"SaleItem(id={self.id}, stock_id={self.stock_id}, quantity={self.quantity}, perprice={self.perprice}, totalprice={self.totalprice})"
