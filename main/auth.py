from flask import render_template, request, flash, url_for, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from models import User

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    print("email = "+email.__str__())

    if User.find_by_email(email=email):
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=name, password=generate_password_hash(password, method='sha256'))

    User.create(new_user)

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.find_by_email(email=email)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('taskbum.profile'))
