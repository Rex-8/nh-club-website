import sqlite3
import os

DATABASE_FILE = os.path.join('database', 'site.db')

def get_db_connection():
    """ Establish a connection to the SQLite database. """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows access to columns by name.
    return conn

def init_db():
    """ Initialize the database tables if they don't exist. """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create members table (formerly authors table)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bio TEXT,
        linkedin_url TEXT,
        portfolio_url TEXT,
        github_url TEXT,
        join_year DATE,
        exit_year DATE
        );
    ''')

    # Create blogs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            thumbnail TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            date_posted TEXT,
            content TEXT NOT NULL
        );
    ''')

    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            thumbnail TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            event_date TEXT,
            content TEXT NOT NULL
        );
    ''')

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            thumbnail TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            date_posted TEXT,
            content TEXT NOT NULL
        );
    ''')

    # Create tags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    ''')

    # Create blog_tags link table (many-to-many relation between blogs and tags)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_tags (
            blog_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (blog_id, tag_id)
        );
    ''')

    # Create event_tags link table (many-to-many relation between events and tags)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_tags (
            event_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (event_id, tag_id)
        );
    ''')

    # Create project_tags link table (many-to-many relation between projects and tags)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_tags (
            project_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (project_id, tag_id)
        );
    ''')

    # Create blog_authors link table (many-to-many relation between blogs and members)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_authors (
            blog_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (blog_id, member_id)
        );
    ''')

    # Create event_authors link table (many-to-many relation between events and members)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_authors (
            event_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (event_id, member_id)
        );
    ''')

    # Create project_authors link table (many-to-many relation between projects and members)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_authors (
            project_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (project_id, member_id)
        );
    ''')

    # Create assist_blog table (many-to-many relation between blogs and assistants)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assist_blog (
            blog_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (blog_id, member_id)
        );
    ''')

    # Create assist_event table (many-to-many relation between events and assistants)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assist_event (
            event_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (event_id, member_id)
        );
    ''')

    # Create assist_project table (many-to-many relation between projects and assistants)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assist_project (
            project_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (member_id) REFERENCES members(id),
            PRIMARY KEY (project_id, member_id)
        );
    ''')

    conn.commit()
    conn.close()
