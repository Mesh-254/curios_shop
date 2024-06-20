from flask import *
from models.user import User
from flask_login import login_required

user = Blueprint('user', __name__)


@user.route('/login')
def login():
    return render_template('login_pages/login.html')


@user.route('/login_post', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect(url_for('jokamu.admin_route'))
    flash('Please check your login details and try again.', 'danger')
    return redirect(url_for('user.login'))


@user.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    flash("You have been logged out successfully", 'danger')
    # Render the logout confirmation page
    return render_template('/login_pages/logout.html')
