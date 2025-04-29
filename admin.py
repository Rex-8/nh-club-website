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

@admin_bp.route('/edit_member', methods=['GET', 'POST'])
@admin_bp.route('/edit_member/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_member(id=None):
    conn = get_db_connection()
    member = None
    
    if id:  # edit mode
        member = conn.execute('SELECT * FROM members WHERE id = ?', (id,)).fetchone()
        if not member:
            conn.close()
            flash('Member not found.')
            return redirect(url_for('admin.list_members'))

    if request.method == 'POST':
        name = request.form['name']
        profile_pic = request.form['profile_pic']  # Or handle file uploads
        bio = request.form['bio']
        linkedin = request.form['linkedin_url']
        portfolio = request.form['portfolio_url']
        github = request.form['github_url']
        join_year = request.form['join_year']
        exit_year = request.form['exit_year']

        if id:  # update
            conn.execute('''
                UPDATE members
                SET name = ?, profile_pic = ?, bio = ?, linkedin_url = ?, portfolio_url = ?, github_url = ?, join_year = ?, exit_year = ?
                WHERE id = ?
            ''', (name, profile_pic, bio, linkedin, portfolio, github, join_year, exit_year, id))
        else:  # insert new
            conn.execute('''
                INSERT INTO members (name, profile_pic, bio, linkedin_url, portfolio_url, github_url, join_year, exit_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, profile_pic, bio, linkedin, portfolio, github, join_year, exit_year))

        conn.commit()
        conn.close()
        return redirect(url_for('admin.list_members'))

    conn.close()
    return render_template('admin/edit_member.html', member=member)

@admin_bp.route('/delete_member/<int:id>', methods=['POST'])
@admin_required
def delete_member(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM members WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash(f'Member {id} deleted successfully.')
    return redirect(url_for('admin.list_members'))


@admin_bp.route('/edit_tag', methods=['GET', 'POST'])
@admin_bp.route('/edit_tag/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_tag(id=None):
    conn = get_db_connection()
    tag = None

    if id:
        tag = conn.execute('SELECT * FROM tags WHERE id = ?', (id,)).fetchone()
        if not tag:
            conn.close()
            flash("Tag not found.")
            return redirect(url_for('admin.list_tags'))

    if request.method == 'POST':
        name = request.form['name']
        if id:
            conn.execute('UPDATE tags SET name = ? WHERE id = ?', (name, id))
        else:
            conn.execute('INSERT INTO tags (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin.list_tags'))

    conn.close()
    return render_template('admin/edit_tag.html', tag=tag)

@admin_bp.route('/delete_tag/<int:id>', methods=['POST'])
@admin_required
def delete_tag(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tags WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.list_tags'))

@admin_bp.route('/edit_blog', methods=['GET', 'POST'])
@admin_bp.route('/edit_blog/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_blog(id=None):
    conn = get_db_connection()
    blog = None

    if id:
        blog = conn.execute('SELECT * FROM blogs WHERE id = ?', (id,)).fetchone()
        if not blog:
            conn.close()
            flash("Blog not found.")
            return redirect(url_for('admin.list_blogs'))

    if request.method == 'POST':
        title = request.form['title']
        thumbnail = request.form['thumbnail']
        slug = request.form['slug']
        date_posted = request.form['date_posted']
        content = request.form['content']

        if id:
            conn.execute('''
                UPDATE blogs SET title=?, thumbnail=?, slug=?, date_posted=?, content=?
                WHERE id=?
            ''', (title, thumbnail, slug, date_posted, content, id))
        else:
            conn.execute('''
                INSERT INTO blogs (title, thumbnail, slug, date_posted, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, thumbnail, slug, date_posted, content))

        conn.commit()
        conn.close()
        return redirect(url_for('admin.list_blogs'))

    conn.close()
    return render_template('admin/edit_blog.html', blog=blog)

@admin_bp.route('/delete_blog/<int:id>', methods=['POST'])
@admin_required
def delete_blog(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM blogs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.list_blogs'))

@admin_bp.route('/edit_event', methods=['GET', 'POST'])
@admin_bp.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_event(id=None):
    conn = get_db_connection()
    event = None

    if id:
        event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
        if not event:
            conn.close()
            flash("Event not found.")
            return redirect(url_for('admin.list_events'))

    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        event_date = request.form['event_date']
        content = request.form['content']

        if id:
            conn.execute('''
                UPDATE events SET title=?, slug=?, event_date=?, content=? WHERE id=?
            ''', (title, slug, event_date, content, id))
        else:
            conn.execute('''
                INSERT INTO events (title, slug, event_date, content)
                VALUES (?, ?, ?, ?)
            ''', (title, slug, event_date, content))

        conn.commit()
        conn.close()
        return redirect(url_for('admin.list_events'))

    conn.close()
    return render_template('admin/edit_event.html', event=event)

@admin_bp.route('/delete_event/<int:id>', methods=['POST'])
@admin_required
def delete_event(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.list_events'))

@admin_bp.route('/edit_project', methods=['GET', 'POST'])
@admin_bp.route('/edit_project/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_project(id=None):
    conn = get_db_connection()
    project = None

    if id:
        project = conn.execute('SELECT * FROM projects WHERE id = ?', (id,)).fetchone()
        if not project:
            conn.close()
            flash("Project not found.")
            return redirect(url_for('admin.list_projects'))

    if request.method == 'POST':
        title = request.form['title']
        thumbnail = request.form['thumbnail']
        slug = request.form['slug']
        date_posted = request.form['date_posted']
        content = request.form['content']

        if id:
            conn.execute('''
                UPDATE projects SET title=?, thumbnail=?, slug=?, date_posted=?, content=? WHERE id=?
            ''', (title, thumbnail, slug, date_posted, content, id))
        else:
            conn.execute('''
                INSERT INTO projects (title, thumbnail, slug, date_posted, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, thumbnail, slug, date_posted, content))

        conn.commit()
        conn.close()
        return redirect(url_for('admin.list_projects'))

    conn.close()
    return render_template('admin/edit_project.html', project=project)

@admin_bp.route('/delete_project/<int:id>', methods=['POST'])
@admin_required
def delete_project(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.list_projects'))
