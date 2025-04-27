from flask import Flask, render_template,send_from_directory
from utils.db_utils import init_db, get_db_connection

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/content/<path:filename>')
def content_static(filename):
    return send_from_directory('content', filename)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/members')
def list_members():
    conn = get_db_connection()

    # Fetch all members
    members = conn.execute('SELECT * FROM members').fetchall()
    
    conn.close()
    return render_template('members.html', members=members)

@app.route('/member/<int:id>')
def view_member(id):
    conn = get_db_connection()

    # Fetch member details
    member = conn.execute('SELECT * FROM members WHERE id = ?', (id,)).fetchone()

    # Fetch member's works (blogs, events, and projects)
    blogs = conn.execute('''
        SELECT b.title, b.slug, b.date_posted
        FROM blogs b
        JOIN blog_authors ba ON ba.blog_id = b.id
        WHERE ba.member_id = ?
    ''', (id,)).fetchall()

    events = conn.execute('''
        SELECT e.title, e.slug, e.event_date
        FROM events e
        JOIN event_authors ea ON ea.event_id = e.id
        WHERE ea.member_id = ?
    ''', (id,)).fetchall()

    projects = conn.execute('''
        SELECT p.title, p.slug, p.date_posted
        FROM projects p
        JOIN project_authors pa ON pa.project_id = p.id
        WHERE pa.member_id = ?
    ''', (id,)).fetchall()

    conn.close()

    if member is None:
        return "Member not found", 404

    return render_template('view_member.html', member=member, blogs=blogs, events=events, projects=projects)

@app.route('/tags')
def list_tags():
    conn = get_db_connection()
    
    # Fetch all tags
    tags = conn.execute('SELECT * FROM tags').fetchall()
    
    conn.close()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:id>')
def view_tag(id):
    conn = get_db_connection()
    
    # Fetch tag details
    tag = conn.execute('SELECT * FROM tags WHERE id = ?', (id,)).fetchone()
    
    # Fetch associated blogs
    blogs = conn.execute('''
        SELECT b.title, b.slug, b.date_posted
        FROM blogs b
        JOIN blog_tags bt ON bt.blog_id = b.id
        WHERE bt.tag_id = ?
    ''', (id,)).fetchall()

    # Fetch associated events
    events = conn.execute('''
        SELECT e.title, e.slug, e.event_date
        FROM events e
        JOIN event_tags et ON et.event_id = e.id
        WHERE et.tag_id = ?
    ''', (id,)).fetchall()

    # Fetch associated projects
    projects = conn.execute('''
        SELECT p.title, p.slug, p.date_posted
        FROM projects p
        JOIN project_tags pt ON pt.project_id = p.id
        WHERE pt.tag_id = ?
    ''', (id,)).fetchall()
    
    conn.close()
    
    if tag is None:
        return "Tag not found", 404
    
    return render_template('view_tags.html', tag=tag, blogs=blogs, events=events, projects=projects)

@app.route('/blogs')
def list_blogs():
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM blogs ORDER BY date_posted DESC').fetchall()
    conn.close()
    return render_template('blogs.html', blogs=blogs)

# View individual blog
@app.route('/blogs/<slug>')
def view_blog(slug):
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE slug = ?', (slug,)).fetchone()

    if blog is None:
        return "Blog not found", 404

    # Fetch tags for the blog
    tags = conn.execute('''
        SELECT tags.id, tags.name FROM tags
        JOIN blog_tags ON blog_tags.tag_id = tags.id
        JOIN blogs ON blogs.id = blog_tags.blog_id
        WHERE blogs.slug = ?
    ''', (slug,)).fetchall()

    # Fetch associated authors for the blog
    authors = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN blog_authors ON members.id = blog_authors.member_id
        WHERE blog_authors.blog_id = ?
    ''', (blog['id'],)).fetchall()

    # Fetch assistants for the blog
    assistants = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN assist_blog ON members.id = assist_blog.member_id
        WHERE assist_blog.blog_id = ?
    ''', (blog['id'],)).fetchall()

    conn.close()
    return render_template('view_blog.html', blog=blog, tags=tags, authors=authors, assistants=assistants)

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

    if project is None:
        return "Project not found", 404

    # Fetch tags for the project
    tags = conn.execute('''
        SELECT tags.id, tags.name FROM tags
        JOIN project_tags ON project_tags.tag_id = tags.id
        JOIN projects ON projects.id = project_tags.project_id
        WHERE projects.slug = ?
    ''', (slug,)).fetchall()

    # Fetch associated authors for the project
    authors = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN project_authors ON members.id = project_authors.member_id
        WHERE project_authors.project_id = ?
    ''', (project['id'],)).fetchall()

    # Fetch assistants for the project
    assistants = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN assist_project ON members.id = assist_project.member_id
        WHERE assist_project.project_id = ?
    ''', (project['id'],)).fetchall()

    conn.close()
    return render_template('view_project.html', project=project, tags=tags, authors=authors, assistants=assistants)

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
    tags = conn.execute('''
        SELECT t.id, t.name FROM tags t 
        JOIN event_tags et ON t.id = et.tag_id 
        WHERE et.event_id = ?
    ''', (event['id'],)).fetchall()

    # Fetch authors for the event
    authors = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN event_authors ON members.id = event_authors.member_id
        WHERE event_authors.event_id = ?
    ''', (event['id'],)).fetchall()

    # Fetch assistants for the event
    assistants = conn.execute('''
        SELECT members.id, members.name, members.bio
        FROM members
        JOIN assist_event ON members.id = assist_event.member_id
        WHERE assist_event.event_id = ?
    ''', (event['id'],)).fetchall()

    conn.close()
    return render_template('view_event.html', event=event, tags=tags, authors=authors, assistants=assistants)

if __name__ == '__main__':
    app.run(debug=True)
