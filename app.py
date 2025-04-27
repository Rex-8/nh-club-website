from flask import Flask, render_template
from utils.db_utils import init_db, get_db_connection

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blogs')
def list_blogs():
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM blogs ORDER BY date_posted DESC').fetchall()
    conn.close()
    return render_template('blogs.html', blogs=blogs)

@app.route('/blogs/<slug>')
def view_blog(slug):
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE slug = ?', (slug,)).fetchone()
    conn.close()
    if blog is None:
        return "Blog not found", 404
    return render_template('blog_detail.html', blog=blog)

@app.route('/projects')
def list_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects ORDER BY date_posted DESC').fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

# View individual project
@app.route('/projects/<slug>')
def view_project(slug):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE slug = ?', (slug,)).fetchone()
    conn.close()
    if project is None:
        return "Project not found", 404
    return render_template('project_detail.html', project=project)

@app.route('/events')
def list_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY event_date DESC').fetchall()
    conn.close()
    return render_template('events.html', events=events)

# View individual event
@app.route('/events/<slug>')
def view_event(slug):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE slug = ?', (slug,)).fetchone()
    conn.close()
    if event is None:
        return "Event not found", 404
    return render_template('event_detail.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
