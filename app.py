from flask import *
from flask_login import LoginManager

from blueprints.routes import jokamu
from blueprints.user import user
from models.database import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from forms.forms import ProductForm
from werkzeug.utils import secure_filename

from models.purchase_items import PurchaseItem, SaleItem
from models.stock import Stock

from models.user import User
from models.products import Product, Category

app = Flask(__name__, static_url_path='/static')

app.url_map.strict_slashes = False

app.register_blueprint(jokamu, url_prefix='/')
app.register_blueprint(user, url_prefix='/')

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_SERVER = os.getenv('DB_SERVER')
app.config['SECRET_KEY'] = os.getenv("MY_SECRET")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', 'jpeg']
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

#  Flask-Login needs to be created and initialized
login = LoginManager(app)


# User Loader Function
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
        category_id = form.category.data  # Assuming category is stored as an ID

        image = form.image.data  # Save uploaded image and get its file path

        # statements to save image in uploads foder
        if image.filename != '':
            uploaded_file = secure_filename(image.filename)
            file_ext = os.path.splitext(uploaded_file)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash('File type not allowed. Please upload a different file type.', 'error')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file))
        new_product = Product(name=name, image=uploaded_file, price=price, description=description,
                              category_id=category_id)
        # Add the product to the database
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('jokamu.view_products'))  # Redirect to edit product page or any other page
    return render_template('admin_pages/edit_product.html', form=form)


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/del_product')
def del_product():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = Product.query.order_by(Product.id.desc())
    queryset = db.paginate(query, page=page, per_page=per_page, error_out=False)
    num_pages = queryset.pages
    next_url = url_for('jokamu.view_products', page=queryset.next_num) \
        if queryset.has_next else None
    prev_url = url_for('jokamu.view_products', page=queryset.prev_num) \
        if queryset.has_prev else None
    return render_template('products_services/delete_product.html', queryset=queryset.items, num_pages=num_pages,
                           next_url=next_url, prev_url=prev_url)


@app.route('/delete_product/<int:id>', methods =['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.image:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image))
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Item/Product deleted successfully!', 'success')
        return redirect(url_for('del_product'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
