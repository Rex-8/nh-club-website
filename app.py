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

    # Fetch tags for the blog
    tags = conn.execute('''
        SELECT tags.name FROM tags
        JOIN blog_tags ON blog_tags.tag_id = tags.id
        JOIN blogs ON blogs.id = blog_tags.blog_id
        WHERE blogs.slug = ?
    ''', (slug,)).fetchall()
    # Fetch associated authors for the blog
    authors = conn.execute('''
        SELECT authors.id, authors.name, authors.bio
        FROM authors
        JOIN blog_authors ON authors.id = blog_authors.author_id
        WHERE blog_authors.blog_id = ?
    ''', (blog['id'],)).fetchall()

    conn.close()

    if blog is None:
        return "Blog not found", 404
    return render_template('view_blog.html', blog=blog, tags=tags,authors = authors)

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

    # Fetch tags for the project
    tags = conn.execute('''
        SELECT tags.name FROM tags
        JOIN project_tags ON project_tags.tag_id = tags.id
        JOIN projects ON projects.id = project_tags.project_id
        WHERE projects.slug = ?
    ''', (slug,)).fetchall()
    # Fetch associated authors for the project
    authors = conn.execute('''
        SELECT authors.id, authors.name, authors.bio
        FROM authors
        JOIN project_authors ON authors.id = project_authors.author_id
        WHERE project_authors.project_id = ?
    ''', (project['id'],)).fetchall()

    conn.close()

    if project is None:
        return "Project not found", 404
    return render_template('view_project.html', project=project, tags=tags,authors = authors)

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
    if event is None:
        return "Event not found", 404
    # Extract tags related to this event (if applicable)
    tags = conn.execute('SELECT t.name FROM tags t JOIN event_tags et ON t.id = et.tag_id WHERE et.event_id = ?', (event['id'],)).fetchall()
    authors = conn.execute('''
        SELECT authors.id, authors.name, authors.bio
        FROM authors
        JOIN event_authors ON authors.id = event_authors.author_id
        WHERE event_authors.event_id = ?
    ''', (event['id'],)).fetchall()
    conn.close()
    return render_template('view_event.html', event=event, tags=tags,authors = authors)

if __name__ == '__main__':
    app.run(debug=True)
