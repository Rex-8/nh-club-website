import hashlib
from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
import sqlite3
from utils.db_utils import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_admin_db_connection():
    conn = sqlite3.connect('database/admin_site.db')
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/')
def admin_home():
    if session.get('admin'):
        return redirect(url_for('admin.admin_tables'))
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin'):
        return redirect(url_for('admin.admin_tables'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_admin_db_connection()
        admin = conn.execute(
            "SELECT * FROM admin_users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        ).fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            return redirect(url_for('admin.admin_tables'))
        flash("Invalid username or password")

    return render_template('admin/login.html')

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route('/tables')
@admin_required
def admin_tables():
    # List of tables to be displayed in the admin panel
    tables = [
        {'name': 'Members', 'url': url_for('admin.list_members')},
        {'name': 'Blogs', 'url': url_for('admin.list_blogs')},
        {'name': 'Events', 'url': url_for('admin.list_events')},
        {'name': 'Projects', 'url': url_for('admin.list_projects')},
        {'name': 'Tags', 'url': url_for('admin.list_tags')}
    ]
    return render_template('admin/tables.html', tables=tables)

@admin_bp.route('/list_members')
@admin_required
def list_members():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    conn.close()
    return render_template('admin/list_members.html', members=members)

@admin_bp.route('/list_blogs')
@admin_required
def list_blogs():
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM blogs').fetchall()  # Fetch all blogs from the database
    conn.close()
    return render_template('admin/list_blogs.html', blogs=blogs)

@admin_bp.route('/list_events')
@admin_required
def list_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()  # Fetch all events from the database
    conn.close()
    return render_template('admin/list_events.html', events=events)

@admin_bp.route('/list_projects')
@admin_required
def list_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()  # Fetch all projects from the database
    conn.close()
    return render_template('admin/list_projects.html', projects=projects)

@admin_bp.route('/list_tags')
@admin_required
def list_tags():
    conn = get_db_connection()
    tags = conn.execute('SELECT * FROM tags').fetchall()  # Fetch all tags from the database
    conn.close()
    return render_template('admin/list_tags.html', tags=tags)
