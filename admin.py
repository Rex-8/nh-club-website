import hashlib
from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
import sqlite3

# Create a Blueprint for admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/a1b2c3d4')  # URL prefix to obscure admin path

# Connect to the admin database
def get_admin_db_connection():
    conn = sqlite3.connect('database/admin_site.db')  # Path to the admin database
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Admin login route
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form['code']
        hash_val = hashlib.sha256(code.encode()).hexdigest()

        conn = get_admin_db_connection()
        result = conn.execute("SELECT * FROM admin_codes WHERE code_hash = ?", (hash_val,)).fetchone()
        conn.close()

        if result:
            session['admin'] = True
            return redirect(url_for('admin.admin_dashboard'))
        flash("Invalid code")
    return render_template('admin/login.html')

# Protect admin routes
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper

# Admin dashboard route
@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
