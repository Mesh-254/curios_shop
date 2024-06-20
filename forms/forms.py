from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DecimalField, TextAreaField, FloatField, TextAreaField, \
    FileField
from wtforms.validators import InputRequired, NumberRange, Length, Regexp, Email, DataRequired
from models.stock import Stock
from models.purchase_items import Supplier
from models.products import Category, Product
from flask_wtf.file import FileField, FileAllowed


class SelectSupplierForm(FlaskForm):
    supplier = SelectField('Supplier', coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supplier.choices = [(supplier.id, supplier.name) for supplier in
                                 Supplier.query.filter_by(is_deleted=False)]


class SupplierForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50),
                                           Regexp('[a-zA-Z\s]+', message='Alphabets and Spaces only')])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=10, max=10),
                                             Regexp('^\d{10}$', message='Numbers only')])
    address = TextAreaField('Address', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])


class StockForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PurchaseItemForm(FlaskForm):
    stock = SelectField('Stock', validators=[InputRequired()], coerce=int)
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0)])
    perprice = DecimalField('Per Price', validators=[InputRequired(), NumberRange(min=0)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock.choices = [(stock.id, stock.name) for stock in Stock.query.filter_by(is_deleted=False)]


class SaleItemForm(FlaskForm):
    stock = SelectField('Stock', validators=[InputRequired()], coerce=int)
    quantity = IntegerField('Quantity', validators=[InputRequired()], render_kw={'min': '0'}, default=0)
    perprice = DecimalField('Per Price', validators=[InputRequired()], render_kw={'min': '0'}, default=0.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock.choices = [(stock.id, stock.name) for stock in Stock.query.filter_by(is_deleted=False).all()]


# Define Product Form
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=1)])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
