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

    # Insert authors
    authors = [
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
    cursor.executemany('INSERT INTO authors (name, bio) VALUES (?, ?);', authors)

    # Insert tags
    tags = [
        ('AI',), ('Machine Learning',), ('Deep Learning',),
        ('Computer Vision',), ('NLP',), ('Robotics',),
        ('Data Science',), ('Ethics',), ('Automation',), ('Healthcare AI',)
    ]
    cursor.executemany('INSERT INTO tags (name) VALUES (?);', tags)

    # Insert blogs
    blogs = [
        ('Intro to AI', 'intro-to-ai', '2025-04-01', 'Introduction to Artificial Intelligence.'),
        ('Deep Learning Advances', 'deep-learning-advances', '2025-04-02', 'Recent advancements in deep learning.'),
        ('Computer Vision Techniques', 'computer-vision-techniques', '2025-04-03', 'Techniques used in computer vision.'),
        ('Natural Language Processing', 'natural-language-processing', '2025-04-04', 'Overview of NLP.'),
        ('Building Robots', 'building-robots', '2025-04-05', 'How to build functional robots.'),
        ('Ethics in AI', 'ethics-in-ai', '2025-04-06', 'Discussion on AI ethics.'),
        ('Healthcare AI', 'healthcare-ai', '2025-04-07', 'Using AI in healthcare.'),
        ('Autonomous Vehicles', 'autonomous-vehicles', '2025-04-08', 'Self-driving car technologies.'),
        ('Data Science Trends', 'data-science-trends', '2025-04-09', 'Trends in data science.'),
        ('AI in Daily Life', 'ai-in-daily-life', '2025-04-10', 'Applications of AI in everyday life.')
    ]
    cursor.executemany('INSERT INTO blogs (title, slug, date_posted, content) VALUES (?, ?, ?, ?);', blogs)

    # Insert events
    events = [
        ('AI Workshop', 'ai-workshop', '2025-05-10', 'A beginner-friendly workshop on AI.'),
        ('ML Hackathon', 'ml-hackathon', '2025-05-20', 'A hackathon focused on ML solutions.'),
        ('Deep Learning Summit', 'deep-learning-summit', '2025-06-15', 'Conference on deep learning research.'),
        ('Robotics Expo', 'robotics-expo', '2025-07-01', 'Showcase of robotics projects.'),
        ('Healthcare AI Conference', 'healthcare-ai-conference', '2025-07-20', 'AI applications in healthcare.'),
        ('Data Science Bootcamp', 'data-science-bootcamp', '2025-08-05', 'Intensive data science training.'),
        ('NLP Workshop', 'nlp-workshop', '2025-08-25', 'Workshop focused on NLP.'),
        ('Automation Fair', 'automation-fair', '2025-09-10', 'Automation technologies exhibition.'),
        ('Ethics Panel', 'ethics-panel', '2025-09-25', 'Panel discussion on AI ethics.'),
        ('Vision Tech Expo', 'vision-tech-expo', '2025-10-05', 'Latest in computer vision tech.')
    ]
    cursor.executemany('INSERT INTO events (title, slug, event_date, content) VALUES (?, ?, ?, ?);', events)

    # Insert projects
    projects = [
        ('AI Chatbot', 'ai-chatbot', '2025-03-01', 'An AI-powered chatbot project.'),
        ('Self-driving Car Prototype', 'self-driving-car-prototype', '2025-03-10', 'Prototype of a self-driving car.'),
        ('Face Recognition System', 'face-recognition-system', '2025-03-20', 'Face recognition security system.'),
        ('NLP Summarizer', 'nlp-summarizer', '2025-03-30', 'Text summarization tool.'),
        ('Healthcare Diagnosis AI', 'healthcare-diagnosis-ai', '2025-04-05', 'AI for diagnosing diseases.'),
        ('Warehouse Robot', 'warehouse-robot', '2025-04-10', 'Autonomous warehouse robot.'),
        ('Data Science Platform', 'data-science-platform', '2025-04-15', 'Integrated data science platform.'),
        ('Autonomous Drone', 'autonomous-drone', '2025-04-20', 'Drone with auto-navigation.'),
        ('Medical Imaging AI', 'medical-imaging-ai', '2025-04-25', 'AI for analyzing medical images.'),
        ('AI Financial Advisor', 'ai-financial-advisor', '2025-04-30', 'Personal finance assistant AI.')
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

    conn.commit()
    conn.close()
    print("✅ Dummy data inserted successfully!")

if __name__ == "__main__":
    populate_dummy_data()
