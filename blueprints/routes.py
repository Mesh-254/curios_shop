import os

from datetime import datetime, timedelta
from flask import abort
import app
from flask import *
from forms.forms import (StockForm, PurchaseItemForm, SaleItemForm, CategoryForm,
                         SupplierForm, SelectSupplierForm, ProductForm)

from models.database import db
from models.stock import Stock
from models.purchase_items import PurchaseItem, SaleItem, Supplier
from models.products import Product, Category
from flask_login import login_required

jokamu = Blueprint('jokamu', __name__)


@jokamu.route('/')
@jokamu.route('/index')
def index():
    queryset = Product.query.order_by(Product.id.desc()).limit(3)
    images = Product.query.all()
    return render_template('index.html', queryset=queryset, images=images)


@jokamu.route('/admin')
def admin_route():
    return redirect(url_for('jokamu.home'))
    # return render_template('/admin_pages/base.html')


@jokamu.route('/home')
def home():
    stock_data = Stock.query.order_by(Stock.id).all()
    labels = [stock.name for stock in stock_data] 
    values = [stock.quantity for stock in stock_data]

    # Sales and purchases
    sales = SaleItem.query.order_by(SaleItem.date.desc()).limit(5)
    purchases = PurchaseItem.query.order_by(PurchaseItem.date.desc()).limit(5)

    return render_template('admin_pages/home.html', labels=labels, values=values,
                           sales=sales, purchases=purchases
                           )


@jokamu.route('/get_sales_and_purchases_per_day')
def get_sales_and_purchases_per_day():
    # Query to fetch total volume of sales per day
    # Calculate the date range for the past 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=29)

    # Initialize lists to store sales and purchases volume and labels
    sales_per_day_values = []
    purchases_per_day_values = []
    labels = []

    # Iterate over each day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Query SaleItems for the current day and sum up the quantities
        total_sales_quantity = sum(item.quantity for item in SaleItem.query.filter(
            SaleItem.date >= current_date,
            SaleItem.date < current_date + timedelta(days=1)
        ))

        # Query PurchaseItems for the current day and sum up the quantities
        total_purchases_quantity = sum(item.quantity for item in PurchaseItem.query.filter(
            PurchaseItem.date >= current_date,
            PurchaseItem.date < current_date + timedelta(days=1)
        ))

        # Append the total sales and purchases quantities and date to the respective lists
        sales_per_day_values.append(total_sales_quantity)
        purchases_per_day_values.append(total_purchases_quantity)
        labels.append(current_date.strftime("%Y-%m-%d"))  # Format the date as needed

        # Move to the next day
        current_date += timedelta(days=1)

    return render_template('admin_pages/chartsjs.html', sales_values=sales_per_day_values,
                           purchases_values=purchases_per_day_values, labels=labels)


@jokamu.route('/get_stock')
def get_stock():
    """Method to fetch all stock records"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = Stock.query.order_by(Stock.id.desc())
    queryset = query.paginate(page=page, per_page=per_page, error_out=False)
    num_pages = queryset.pages
    next_url = url_for('jokamu.get_stock', page=queryset.next_num) \
        if queryset.has_next else None
    prev_url = url_for('jokamu.get_stock', page=queryset.prev_num) \
        if queryset.has_prev else None
    return render_template('/admin_pages/inventory.html', queryset=queryset.items, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


@jokamu.route('/search_stock', methods=['GET'])
def search_stock():
    query = request.args.get('query')
    if query:
        queryset = Stock.query.filter(Stock.name.icontains(query)).order_by(Stock.id.desc())
    else:
        queryset = []
    return render_template('admin_pages/search_stock.html', queryset=queryset)


@jokamu.route('/add_stock', methods=['POST', 'GET'])
def add_stock():
    form = StockForm()
    if form.validate_on_submit():
        stock_exists = Stock.query.filter(Stock.name == form.name.data).first()
        if stock_exists:
            flash('This stock item already exists !', 'danger')
            return redirect(url_for('jokamu.add_stock'))
        new_stock = Stock(
            name=form.name.data,
            quantity=form.quantity.data
        )
        # Add the new record to the database session
        db.session.add(new_stock)
        # Commit the session to save the changes to the database
        db.session.commit()
        # Redirect to a different page after adding the record
        flash('New Stock Item added successfully!', 'success')
        return redirect(url_for('jokamu.get_stock'))
    return render_template('/admin_pages/edit_stock.html', title='Stock', form=form)


@jokamu.route('/edit_stock/<int:id>', methods=['GET', 'POST'])
def edit_stock(id):
    stock = Stock.query.get_or_404(id)
    form = StockForm(obj=stock)
    if form.validate_on_submit():
        stock.name = form.name.data
        stock.quantity = form.quantity.data
        db.session.commit()
        flash('Stock updated successfully!', 'success')
        return redirect(url_for('jokamu.get_stock'))
    return render_template('/admin_pages/edit_stock.html', title='Edit Stock', form=form)


@jokamu.route('/delete_stock/<int:id>', methods=['GET', 'POST'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(stock)
        db.session.commit()
        flash('Stock Item deleted successfully!', 'success')
        return redirect(url_for('jokamu.get_stock'))
    return render_template('/admin_pages/confirm_delete_stock.html', stock=stock)


@jokamu.route('/suppliers_list')
def suppliers_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = Supplier.query.filter_by(is_deleted=False).order_by(Supplier.id.desc())
    suppliers = query.paginate(page=page, per_page=per_page, error_out=False)
    num_pages = suppliers.page
    next_url = url_for('jokamu.suppliers_list', page=suppliers.next_num) \
        if suppliers.has_next else None
    prev_url = url_for('jokamu.suppliers_list', page=suppliers.prev_num) \
        if suppliers.has_prev else None
    return render_template('admin_pages/suppliers_list.html', suppliers=suppliers, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


@jokamu.route('/search_supplier', methods=['GET'])
def search_supplier():
    query = request.args.get('q')
    if query:
        queryset = Supplier.query.filter(
            Supplier.name.icontains(query) | Supplier.phone.icontains(query) | Supplier.email.icontains(
                query)).order_by(Supplier.id.desc())
    else:
        queryset = []
    return render_template('admin_pages/search_supplier.html', queryset=queryset)


@jokamu.route('/create_supplier', methods=['POST', 'GET'])
def create_supplier():
    title = "New Supplier"
    form = SupplierForm()
    if form.validate_on_submit():
        phone_or_email_exists = Supplier.query.filter(
            (Supplier.phone == form.phone.data) | (Supplier.email == form.email.data)
            | (Supplier.name == form.name.data)).first()
        if phone_or_email_exists:
            flash('That phone number or email has been used before!', 'danger')
            return redirect(url_for('jokamu.create_supplier'))
        new_supplier = Supplier(
            name=form.name.data,
            phone=form.phone.data,
            address=form.address.data,
            email=form.email.data,
        )
        db.session.add(new_supplier)
        db.session.commit()
        flash('You have successfully created a New Supplier', 'success')
        return redirect(url_for('jokamu.suppliers_list'))
    return render_template('admin_pages/edit_supplier.html', title=title, form=form)


@jokamu.route('/update_supplier/<int:id>', methods=['POST', 'GET'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        supplier.name = form.name.data,
        supplier.phone = form.phone.data,
        supplier.address = form.address.data,
        supplier.email = form.email.data,
        db.session.commit()
        flash('Supplier has been updated successfully', 'success')
        return redirect(url_for('jokamu.suppliers_list'))
    return render_template('admin_pages/edit_supplier.html', form=form, supplier=supplier)


@jokamu.route('/delete_supplier/<int:id>', methods=['POST', 'GET'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        # Soft delete: Mark the supplier as deleted instead of removing it from the database
        supplier.is_deleted = True
        db.session.commit()
        flash('You have deleted the supplier successfully', 'success')
        return redirect(url_for('jokamu.suppliers_list'))
    return render_template('admin_pages/delete_supplier.html', supplier=supplier)


@jokamu.route('/supplier_details/<int:id>')
def supplier_details(id):
    supplier_info = Supplier.query.get_or_404(id)
    supplier_purchases = supplier_info.purchase_items  # Fetch all purchases made by the supplier
    return render_template('admin_pages/supplier.html', supplier_info=supplier_info,
                           supplier_purchases=supplier_purchases)


@jokamu.route('/select_supplier', methods=['GET', 'POST'])
def select_supplier():
    form = SelectSupplierForm()
    # Filter suppliers where is_deleted is False
    form.supplier.choices = [(supplier.id, supplier.name) for supplier in
                             Supplier.query.filter_by(is_deleted=False).all()]
    if form.validate_on_submit():
        supplier_id = form.supplier.data
        return redirect(url_for('jokamu.new_purchase', supplier_id=supplier_id))
    return render_template('admin_pages/select_supplier.html', form=form)


@jokamu.route('/new_purchase/<int:supplier_id>', methods=['GET', 'POST'])
def new_purchase(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = PurchaseItemForm()
    if form.validate_on_submit():
        # Fetch the Stock object based on the selected stock ID
        stock_item = Stock.query.get(form.stock.data)

        # Calculate total price
        total_price = form.quantity.data * form.perprice.data

        # Check if the quantity is available in stock
        if stock_item.quantity:
            # add the purchased quantity to stock quantity
            stock_item.quantity += form.quantity.data

        # Create a new purchase item with the calculated total price
        new_purchase = PurchaseItem(
            stock=stock_item,
            quantity=form.quantity.data,
            perprice=form.perprice.data,
            totalprice=total_price,
            supplier=supplier
        )
        db.session.add(new_purchase)
        db.session.commit()
        flash('You have created a purchase successfully', 'success')
        return redirect(url_for('jokamu.view_purchases'))
    return render_template('/admin_pages/new_purchase.html', form=form)


@jokamu.route('/view_purchases')
def view_purchases():
    # Assume bills contains the list of purchases
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = PurchaseItem.query.order_by(PurchaseItem.id.desc())
    bills = query.paginate(page=page, per_page=per_page, error_out=False)
    num_pages = bills.pages
    next_url = url_for('jokamu.view_purchases', page=bills.next_num) \
        if bills.has_next else None
    prev_url = url_for('jokamu.view_purchases', page=bills.prev_num) \
        if bills.has_prev else None
    return render_template('/admin_pages/purchase_list.html', bills=bills.items, next_url=next_url, prev_url=prev_url,
                           num_pages=num_pages)


@jokamu.route('/search_purchase', methods=['GET'])
def search_purchase():
    query = request.args.get('q')
    if query:
        queryset = PurchaseItem.query.join(Stock).join(Supplier).filter(
            Stock.name.icontains(query) | PurchaseItem.date.icontains(query) | Supplier.name.icontains(
                query)).order_by(
            PurchaseItem.date.desc()).all()
    else:
        queryset = []
        # queryset = PurchaseItem.query.filter(PurchaseItem.stock.icontains(query).order_by(
        #         PurchaseItem.date.desc()))
    return render_template('admin_pages/search_purchase.html', queryset=queryset)


@jokamu.route('/view_purchase_bill/<int:id>')
def view_purchase_bill(id):
    bill = PurchaseItem.query.get_or_404(id)
    return render_template('/admin_pages/bill_base.html', bill=bill)


@jokamu.route('/view_sale_bill/<int:id>')
def view_sale_bill(id):
    bill = SaleItem.query.get_or_404(id)
    return render_template('/admin_pages/sale_bill.html', bill= bill)


@jokamu.route('/delete_purchase_bill/<int:id>', methods=['GET', 'POST'])
def delete_purchase_bill(id):
    bill = PurchaseItem.query.get_or_404(id)
    if request.method == 'POST':
        update_purchase_stock_quantity(bill)
        db.session.delete(bill)
        db.session.commit()
        flash("You have successfully deleted bill", "danger")
        return redirect(url_for('jokamu.view_purchases'))
    return render_template('/admin_pages/delete_purchase_bill.html', bill=bill)


#  decreases the stock quantity of an item if the purchase is deleted:
def update_purchase_stock_quantity(purchase_item):
    stock_item = purchase_item.stock
    stock_item.quantity -= purchase_item.quantity
    db.session.commit()


@jokamu.route('/new_sale', methods=['POST', 'GET'])
def new_sale():
    form = SaleItemForm()
    if form.validate_on_submit():
        stock_item = Stock.query.get(form.stock.data)

        total_price = form.quantity.data * form.perprice.data

        # Check if the quantity is available in stock
        if stock_item.quantity:
            # Deduct the purchased quantity from the stock quantity
            stock_item.quantity -= form.quantity.data

        sale_order = SaleItem(
            stock=stock_item,
            quantity=form.quantity.data,
            perprice=form.perprice.data,
            totalprice=total_price
        )
        db.session.add(sale_order)
        db.session.commit()
        flash("You have successfully created a new purchase.", "success")
        return redirect(url_for('jokamu.sales_list'))
    return render_template('/admin_pages/new_sale.html', form=form)


@jokamu.route('sales_list')
def sales_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = SaleItem.query.order_by(SaleItem.id.desc())
    sale_orders = query.paginate(page=page, per_page=per_page, error_out=False)
    num_pages = sale_orders.pages
    next_url = url_for('jokamu.sales_list', page=sale_orders.next_num) \
        if sale_orders.has_next else None
    prev_url = url_for('jokamu.sales_list', page=sale_orders.prev_num) \
        if sale_orders.has_prev else None
    return render_template('admin_pages/sales_list.html', sale_orders=sale_orders, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


@jokamu.route('/search_sale', methods=['GET'])
def search_sale():
    query = request.args.get('q')
    if query:
        queryset = SaleItem.query.join(Stock).filter(
            SaleItem.date.icontains(query) | Stock.name.icontains(query)).order_by(SaleItem.date.desc()).all()
    else:
        queryset = []
    return render_template('admin_pages/search_sale.html', queryset=queryset)


@jokamu.route('/delete_sale/<int:id>', methods=['GET', 'POST'])
def delete_sale(id):
    bill = SaleItem.query.get_or_404(id)

    if request.method == 'POST':
        # Update stock quantity if the sale is deleted
        update_stock_quantity(bill)
        db.session.delete(bill)
        db.session.commit()
        flash("You have successfully deleted sale", "danger")
        return redirect(url_for('jokamu.sales_list'))
    return render_template('/admin_pages/delete_sale.html', bill=bill)


#  increases the stock quantity of an item if the sale is deleted:
def update_stock_quantity(sale_item):
    stock_item = sale_item.stock
    stock_item.quantity += sale_item.quantity
    db.session.commit()


# Route for adding a new category
@jokamu.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data

        # Create new Category instance
        new_category = Category(name=name)

        # Add the category to the database
        db.session.add(new_category)
        db.session.commit()
        flash('You have successfully created a new Category!', 'success')
        return redirect(url_for('jokamu.category_list'))
    return render_template('admin_pages/edit_product_category.html', form=form)


@jokamu.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    queryset = Category.query.get_or_404(id)
    form = CategoryForm(obj=queryset)
    if form.validate_on_submit():
        queryset.name = form.name.data
        db.session.commit()
        flash('Supplier has been updated successfully.', 'alert-success')
        return redirect(url_for('jokamu.category_list'))
    return render_template('admin_pages/edit_product_category.html', form=form)


@jokamu.route('/delete_category/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    queryset = Category.query.get_or_404(id)
    # Check if the category exists
    if queryset is None:
        return jsonify({'error': 'Category not found'}), 404

    # Check if there are any products associated with the category
    if queryset.products:
        flash('You cannot delete this category because it has associated products.', 'danger')
        return redirect(url_for('jokamu.category_list'))

    # Delete the category
    db.session.delete(queryset)
    db.session.commit()
    flash('You have successfully  deleted Category', 'success')
    return redirect(url_for('jokamu.category_list'))


@jokamu.route('/category_list')
def category_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = Category.query.order_by(Category.id.desc())
    queryset = db.paginate(query, page=page, per_page=per_page, error_out=False)
    num_pages = queryset.pages
    next_url = url_for('jokamu.category_list', page=queryset.next_num) \
        if queryset.has_next else None
    prev_url = url_for('jokamu.category_list', page=queryset.prev_num) \
        if queryset.has_prev else None
    return render_template('admin_pages/category_list.html', queryset=queryset.items, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


# Route for adding a new product
@jokamu.route('/view_products')
def view_products():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = Product.query.order_by(Product.id.desc())
    queryset = db.paginate(query, page=page, per_page=per_page, error_out=False)
    num_pages = queryset.pages
    next_url = url_for('jokamu.view_products', page=queryset.next_num) \
        if queryset.has_next else None
    prev_url = url_for('jokamu.view_products', page=queryset.prev_num) \
        if queryset.has_prev else None
    return render_template('products_services/products.html', queryset=queryset.items, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


@jokamu.route('/product_details/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    title = product.name
    similar_products = Product.query.filter_by(category=product.category)
    return render_template('products_services/product_detail.html', product=product, title=title,
                           similar_products=similar_products)
