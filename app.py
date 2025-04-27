from flask import Flask
from utils.db_utils import init_db

app = Flask(__name__)

# Initialize the database
init_db()

# Routes for blogs
@app.route('/blogs')
def list_blogs():
    return "List of all blogs"

@app.route('/blogs/<slug>')
def view_blog(slug):
    return f"View blog with slug: {slug}"

# Routes for events
@app.route('/events')
def list_events():
    return "List of all events"

@app.route('/events/<slug>')
def view_event(slug):
    return f"View event with slug: {slug}"

# Routes for projects
@app.route('/projects')
def list_projects():
    return "List of all projects"

@app.route('/projects/<slug>')
def view_project(slug):
    return f"View project with slug: {slug}"

# Main route
@app.route('/')
def index():
    return "Welcome to the website!"

if __name__ == "__main__":
    app.run(debug=True)
