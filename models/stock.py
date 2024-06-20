from models.database import db
from sqlalchemy.orm import validates


class Stock(db.Model):
    __table_name__ = 'stock'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=True)
    quantity = db.Column(db.Integer, default=1)
    is_deleted = db.Column(db.Boolean, default=False)

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value < 1:
            raise ValueError("Quantity cannot be negative")
        return value

    def __repr__(self):
        return self.name
