import os
import random
import sqlite3

DATABASE_FILE = os.path.join('database', 'site.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def populate_dummy_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert members (authors and assistants)
    members = [
        ('Alice Smith', 'Machine Learning specialist.'),
        ('Bob Johnson', 'Data Scientist and AI enthusiast.'),
        ('Charlie Brown', 'Deep Learning researcher.'),
        ('Diana Prince', 'Computer Vision expert.'),
        ('Evan Wright', 'Robotics engineer.'),
        ('Fiona Lee', 'NLP specialist.'),
        ('George Harris', 'Data Engineer and Analyst.'),
        ('Hannah Adams', 'AI Ethics researcher.'),
        ('Ian Cook', 'Autonomous Systems developer.'),
        ('Jane Foster', 'Medical Imaging expert.')
    ]
    cursor.executemany('INSERT INTO members (name, bio) VALUES (?, ?);', members)

    # Insert tags
    tags = [
        ('AI',), ('Machine Learning',), ('Deep Learning',),
        ('Computer Vision',), ('NLP',), ('Robotics',),
        ('Data Science',), ('Ethics',), ('Automation',), ('Healthcare AI',)
    ]
    cursor.executemany('INSERT INTO tags (name) VALUES (?);', tags)

    # Insert blogs
    blogs = [
        ('Intro to AI', 'blog-1-intro-to-ai', '2025-04-01', 'Introduction to Artificial Intelligence.'),
        ('Deep Learning Advances', 'blog-2-deep-learning-advances', '2025-04-02', 'Recent advancements in deep learning.'),
        ('Computer Vision Techniques', 'blog-3-computer-vision-techniques', '2025-04-03', 'Techniques used in computer vision.'),
        ('Natural Language Processing', 'blog-4-natural-language-processing', '2025-04-04', 'Overview of NLP.'),
        ('Building Robots', 'blog-5-building-robots', '2025-04-05', 'How to build functional robots.'),
        ('Ethics in AI', 'blog-6-ethics-in-ai', '2025-04-06', 'Discussion on AI ethics.'),
        ('Healthcare AI', 'blog-7-healthcare-ai', '2025-04-07', 'Using AI in healthcare.'),
        ('Autonomous Vehicles', 'blog-8-autonomous-vehicles', '2025-04-08', 'Self-driving car technologies.'),
        ('Data Science Trends', 'blog-9-data-science-trends', '2025-04-09', 'Trends in data science.'),
        ('AI in Daily Life', 'blog-10-ai-in-daily-life', '2025-04-10', 'Applications of AI in everyday life.')
    ]
    cursor.executemany('INSERT INTO blogs (title, slug, date_posted, content) VALUES (?, ?, ?, ?);', blogs)

    # Insert events
    events = [
        ('AI Workshop', 'event-1-ai-workshop', '2025-05-10', 'A beginner-friendly workshop on AI.'),
        ('ML Hackathon', 'event-2-ml-hackathon', '2025-05-20', 'A hackathon focused on ML solutions.'),
        ('Deep Learning Summit', 'event-3-deep-learning-summit', '2025-06-15', 'Conference on deep learning research.'),
        ('Robotics Expo', 'event-4-robotics-expo', '2025-07-01', 'Showcase of robotics projects.'),
        ('Healthcare AI Conference', 'event-5-healthcare-ai-conference', '2025-07-20', 'AI applications in healthcare.'),
        ('Data Science Bootcamp', 'event-6-data-science-bootcamp', '2025-08-05', 'Intensive data science training.'),
        ('NLP Workshop', 'event-7-nlp-workshop', '2025-08-25', 'Workshop focused on NLP.'),
        ('Automation Fair', 'event-8-automation-fair', '2025-09-10', 'Automation technologies exhibition.'),
        ('Ethics Panel', 'event-9-ethics-panel', '2025-09-25', 'Panel discussion on AI ethics.'),
        ('Vision Tech Expo', 'event-10-vision-tech-expo', '2025-10-05', 'Latest in computer vision tech.')
    ]
    cursor.executemany('INSERT INTO events (title, slug, event_date, content) VALUES (?, ?, ?, ?);', events)

    # Insert projects
    projects = [
        ('AI Chatbot', 'project-1-ai-chatbot', '2025-03-01', 'An AI-powered chatbot project.'),
        ('Self-driving Car Prototype', 'project-2-self-driving-car-prototype', '2025-03-10', 'Prototype of a self-driving car.'),
        ('Face Recognition System', 'project-3-face-recognition-system', '2025-03-20', 'Face recognition security system.'),
        ('NLP Summarizer', 'project-4-nlp-summarizer', '2025-03-30', 'Text summarization tool.'),
        ('Healthcare Diagnosis AI', 'project-5-healthcare-diagnosis-ai', '2025-04-05', 'AI for diagnosing diseases.'),
        ('Warehouse Robot', 'project-6-warehouse-robot', '2025-04-10', 'Autonomous warehouse robot.'),
        ('Data Science Platform', 'project-7-data-science-platform', '2025-04-15', 'Integrated data science platform.'),
        ('Autonomous Drone', 'project-8-autonomous-drone', '2025-04-20', 'Drone with auto-navigation.'),
        ('Medical Imaging AI', 'project-9-medical-imaging-ai', '2025-04-25', 'AI for analyzing medical images.'),
        ('AI Financial Advisor', 'project-10-ai-financial-advisor', '2025-04-30', 'Personal finance assistant AI.')
    ]
    cursor.executemany('INSERT INTO projects (title, slug, date_posted, content) VALUES (?, ?, ?, ?);', projects)

    # Link blogs to random tags
    for blog_id in range(1, 11):
        tag_ids = random.sample(range(1, 11), 2)
        for tag_id in tag_ids:
            cursor.execute('INSERT INTO blog_tags (blog_id, tag_id) VALUES (?, ?);', (blog_id, tag_id))

    # Link events to random tags
    for event_id in range(1, 11):
        tag_ids = random.sample(range(1, 11), 2)
        for tag_id in tag_ids:
            cursor.execute('INSERT INTO event_tags (event_id, tag_id) VALUES (?, ?);', (event_id, tag_id))

    # Link projects to random tags
    for project_id in range(1, 11):
        tag_ids = random.sample(range(1, 11), 2)
        for tag_id in tag_ids:
            cursor.execute('INSERT INTO project_tags (project_id, tag_id) VALUES (?, ?);', (project_id, tag_id))

    # Link blogs to random authors (members)
    for blog_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random members
        for member_id in member_ids:
            cursor.execute('INSERT INTO blog_authors (blog_id, member_id) VALUES (?, ?);', (blog_id, member_id))

    # Link events to random authors (members)
    for event_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random members
        for member_id in member_ids:
            cursor.execute('INSERT INTO event_authors (event_id, member_id) VALUES (?, ?);', (event_id, member_id))

    # Link projects to random authors (members)
    for project_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random members
        for member_id in member_ids:
            cursor.execute('INSERT INTO project_authors (project_id, member_id) VALUES (?, ?);', (project_id, member_id))

    # Link blogs to random assistants (members)
    for blog_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random assistants
        for member_id in member_ids:
            cursor.execute('INSERT INTO assist_blog (blog_id, member_id) VALUES (?, ?);', (blog_id, member_id))

    # Link events to random assistants (members)
    for event_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random assistants
        for member_id in member_ids:
            cursor.execute('INSERT INTO assist_event (event_id, member_id) VALUES (?, ?);', (event_id, member_id))

    # Link projects to random assistants (members)
    for project_id in range(1, 11):
        member_ids = random.sample(range(1, 11), 2)  # Select 2 random assistants
        for member_id in member_ids:
            cursor.execute('INSERT INTO assist_project (project_id, member_id) VALUES (?, ?);', (project_id, member_id))

    conn.commit()
    conn.close()
    print("✅ Dummy data inserted successfully!")

if __name__ == "__main__":
    populate_dummy_data()
