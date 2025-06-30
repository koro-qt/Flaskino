from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import User
from flask import jsonify

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/update_balance', methods=['POST'])
@login_required
def update_balance():
    data = request.get_json()
    new_balance = data.get('balance')
    if new_balance is not None and isinstance(new_balance, int):
        user = User.get_by_id(current_user.id)
        user.update_balance(new_balance)
        return jsonify({'success': True, 'balance': user.balance})
    return jsonify({'success': False, 'error': 'Invalid balance'}), 400


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        if User.create(username, password, email):
            return redirect(url_for('auth.login'))
        flash('Username already exists.')
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_email = request.form['email']
        current_user.update_profile(new_email)
        flash('Profile updated.')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html', user=current_user)


@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    current_user.delete_account()
    logout_user()
    flash('Account deleted.')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
