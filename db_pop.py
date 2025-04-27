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
        ('Alice Smith', 'Machine Learning specialist.', 'https://linkedin.com/in/alice-smith', 'https://aliceportfolio.com', 'https://github.com/alice-smith', 2020, 2024),
        ('Bob Johnson', 'Data Scientist and AI enthusiast.', 'https://linkedin.com/in/bob-johnson', 'https://bobportfolio.com', 'https://github.com/bob-johnson', 2021, 2025),
        ('Charlie Brown', 'Deep Learning researcher.', 'https://linkedin.com/in/charlie-brown', 'https://charlieportfolio.com', 'https://github.com/charlie-brown', 2020, 2023),
        ('Diana Prince', 'Computer Vision expert.', 'https://linkedin.com/in/diana-prince', 'https://dianaportfolio.com', 'https://github.com/diana-prince', 2022, 2025),
        ('Evan Wright', 'Robotics engineer.', 'https://linkedin.com/in/evan-wright', 'https://evanportfolio.com', 'https://github.com/evan-wright', 2021, 2024),
        ('Fiona Lee', 'NLP specialist.', 'https://linkedin.com/in/fiona-lee', 'https://fionaportfolio.com', 'https://github.com/fiona-lee', 2020, 2023),
        ('George Harris', 'Data Engineer and Analyst.', 'https://linkedin.com/in/george-harris', 'https://georgeportfolio.com', 'https://github.com/george-harris', 2021, 2025),
        ('Hannah Adams', 'AI Ethics researcher.', 'https://linkedin.com/in/hannah-adams', 'https://hannahportfolio.com', 'https://github.com/hannah-adams', 2022, 2025),
        ('Ian Cook', 'Autonomous Systems developer.', 'https://linkedin.com/in/ian-cook', 'https://ianportfolio.com', 'https://github.com/ian-cook', 2020, 2024),
        ('Jane Foster', 'Medical Imaging expert.', 'https://linkedin.com/in/jane-foster', 'https://janesportfolio.com', 'https://github.com/jane-foster', 2021, 2024)
    ]

    cursor.executemany('''
        INSERT INTO members (name, bio, linkedin_url, portfolio_url, github_url, join_year, exit_year)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', members)

    # Insert tags
    tags = [
        ('AI',), ('Machine Learning',), ('Deep Learning',),
        ('Computer Vision',), ('NLP',), ('Robotics',),
        ('Data Science',), ('Ethics',), ('Automation',), ('Healthcare AI',)
    ]
    cursor.executemany('INSERT INTO tags (name) VALUES (?);', tags)

    # Insert blogs 
    blogs = [
        ('Intro to AI', 'blog-1-intro-to-ai', '2025-04-01', '''<p>Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.</p><img src="/content/blog-images/blog-1-image-1.jpg"><p>Over the years, AI has evolved from simple rule-based systems to complex neural networks capable of deep learning and decision making.</p><img src="/content/blog-images/blog-1-image-2.jpg"><p>Today, AI is applied in numerous fields such as healthcare, finance, transportation, and entertainment, transforming industries and our daily lives.</p><p>As AI technology progresses, it also brings ethical challenges and questions about its impact on employment, privacy, and society at large.</p>''', '/content/blog-images/blog-1-thumbnail.jpg'),
        ('Deep Learning Advances', 'blog-2-deep-learning-advances', '2025-04-02', '''<p>Deep learning is a subset of machine learning that uses neural networks with many layers to learn from large amounts of data.</p><img src="/content/blog-images/blog-2-image-1.jpg"><p>This article explores the most recent advancements in deep learning algorithms and their application in real-world problems, such as image recognition, language translation, and autonomous systems.</p><img src="/content/blog-images/blog-2-image-2.jpg">''', '/content/blog-images/blog-2-thumbnail.jpg'),
        ('Computer Vision Techniques', 'blog-3-computer-vision-techniques', '2025-04-03', '''<p>Computer vision enables machines to interpret and understand the visual world. Using digital images from cameras, videos, and sensors, machines can identify and process objects and scenes.</p><img src="/content/blog-images/blog-3-image-1.jpg"><p>This blog delves into the various techniques used in computer vision, including edge detection, object tracking, and image segmentation.</p><img src="/content/blog-images/blog-3-image-2.jpg">''', '/content/blog-images/blog-3-thumbnail.jpg'),
        ('Natural Language Processing', 'blog-4-natural-language-processing', '2025-04-04', '''<p>Natural Language Processing (NLP) involves teaching machines to understand, interpret, and respond to human language.</p><img src="/content/blog-images/blog-4-image-1.jpg"><p>This blog covers the latest NLP techniques such as sentiment analysis, named entity recognition, and language generation.</p><img src="/content/blog-images/blog-4-image-2.jpg">''', '/content/blog-images/blog-4-thumbnail.jpg'),
        ('Building Robots', 'blog-5-building-robots', '2025-04-05', '''<p>Building robots involves integrating hardware and software to create autonomous systems that can perform tasks without human intervention.</p><img src="/content/blog-images/blog-5-image-1.jpg"><p>This blog will guide you through the fundamental principles of building robots, from sensor integration to motion control.</p><img src="/content/blog-images/blog-5-image-2.jpg">''', '/content/blog-images/blog-5-thumbnail.jpg'),
        ('Ethics in AI', 'blog-6-ethics-in-ai', '2025-04-06', '''<p>As artificial intelligence continues to evolve, ethical considerations surrounding its use and impact are becoming more important.</p><img src="/content/blog-images/blog-6-image-1.jpg"><p>This blog discusses the ethical dilemmas in AI, including bias in algorithms, privacy concerns, and the potential consequences of AI-driven decision-making.</p><img src="/content/blog-images/blog-6-image-2.jpg">''', '/content/blog-images/blog-6-thumbnail.jpg'),
        ('Healthcare AI', 'blog-7-healthcare-ai', '2025-04-07', '''<p>AI has the potential to revolutionize healthcare by improving diagnosis, personalizing treatment, and optimizing healthcare workflows.</p><img src="/content/blog-images/blog-7-image-1.jpg"><p>This blog discusses the impact of AI on healthcare, including applications in medical imaging, predictive analytics, and patient care.</p><img src="/content/blog-images/blog-7-image-2.jpg">''', '/content/blog-images/blog-7-thumbnail.jpg'),
        ('Autonomous Vehicles', 'blog-8-autonomous-vehicles', '2025-04-08', '''<p>Autonomous vehicles use sensors and AI algorithms to navigate and operate without human intervention.</p><img src="/content/blog-images/blog-8-image-1.jpg"><p>This blog explores the development of self-driving cars, the technologies that power them, and their potential to transform the transportation industry.</p><img src="/content/blog-images/blog-8-image-2.jpg">''', '/content/blog-images/blog-8-thumbnail.jpg'),
        ('Data Science Trends', 'blog-9-data-science-trends', '2025-04-09', '''<p>Data science is an interdisciplinary field that combines statistical analysis, machine learning, and big data techniques to extract meaningful insights from data.</p><img src="/content/blog-images/blog-9-image-1.jpg"><p>This blog highlights the latest trends in data science, including automation in data analysis, AI-powered analytics, and the growing demand for data science professionals.</p><img src="/content/blog-images/blog-9-image-2.jpg">''', '/content/blog-images/blog-9-thumbnail.jpg'),
        ('AI in Daily Life', 'blog-10-ai-in-daily-life', '2025-04-10', '''<p>AI is becoming an integral part of our daily lives, from virtual assistants to personalized recommendations.</p><img src="/content/blog-images/blog-10-image-1.jpg"><p>This blog explores the various applications of AI that enhance our daily activities, such as smart home devices, voice assistants, and AI-driven entertainment platforms.</p><img src="/content/blog-images/blog-10-image-2.jpg">''', '/content/blog-images/blog-10-thumbnail.jpg')
    ]
    cursor.executemany('INSERT INTO blogs (title, slug, date_posted, content, thumbnail) VALUES (?, ?, ?, ?, ?);', blogs)


    # Insert events 
    events = [
        ('AI Workshop', 'event-1-ai-workshop', '2025-05-10', '''<p>Artificial Intelligence (AI) Workshop is designed for beginners to introduce them to the world of AI.</p><img src="/content/event-images/event-1-image-1.jpg" alt="AI Workshop Image"><p>Through this workshop, participants will learn the basics of AI, including its application in various fields such as healthcare, finance, and robotics.</p><img src="/content/event-images/event-1-image-2.jpg" alt="AI Workshop Participants">''', '/content/event-images/event-1-thumbnail.jpg'),
        ('ML Hackathon', 'event-2-ml-hackathon', '2025-05-20', '''<p>This is a hands-on hackathon where participants will be tasked with building machine learning models for real-world problems.</p><img src="/content/event-images/event-2-image-1.jpg" alt="Hackathon Event Image"><p>Participants will work in teams to create innovative solutions using machine learning algorithms, competing for prizes and recognition.</p>''', '/content/event-images/event-2-thumbnail.jpg'),
        ('Deep Learning Summit', 'event-3-deep-learning-summit', '2025-06-15', '''<p>The Deep Learning Summit brings together industry experts and researchers to discuss the latest advancements in deep learning techniques.</p><img src="/content/event-images/event-3-image-1.jpg" alt="Deep Learning Summit Image"><p>Attendees will get a chance to learn from thought leaders in AI and explore emerging trends in deep learning technologies.</p><img src="/content/event-images/event-3-image-2.jpg" alt="Summit Panel Discussion">''', '/content/event-images/event-3-thumbnail.jpg'),
        ('Robotics Expo', 'event-4-robotics-expo', '2025-07-01', '''<p>The Robotics Expo is an event showcasing cutting-edge robotics technology from around the world.</p><img src="/content/event-images/event-4-image-1.jpg" alt="Robotics Expo Image"><p>From autonomous vehicles to medical robots, attendees will witness the latest innovations in the field of robotics.</p><img src="/content/event-images/event-4-image-2.jpg" alt="Robotics Expo Demonstration">''', '/content/event-images/event-4-thumbnail.jpg'),
        ('Healthcare AI Conference', 'event-5-healthcare-ai-conference', '2025-07-20', '''<p>The Healthcare AI Conference focuses on the application of artificial intelligence in healthcare, such as diagnosis, treatment planning, and drug discovery.</p><img src="/content/event-images/event-5-image-1.jpg" alt="Healthcare AI Image"><p>Experts in AI and healthcare will come together to explore how AI is revolutionizing the healthcare industry.</p><img src="/content/event-images/event-5-image-2.jpg" alt="Healthcare AI Technology">''', '/content/event-images/event-5-thumbnail.jpg'),
        ('Data Science Bootcamp', 'event-6-data-science-bootcamp', '2025-08-05', '''<p>The Data Science Bootcamp is a comprehensive program that equips participants with the skills to analyze and interpret complex data.</p><img src="/content/event-images/event-6-image-1.jpg" alt="Data Science Bootcamp Image"><p>Attendees will gain hands-on experience with tools like Python, R, and machine learning algorithms.</p><img src="/content/event-images/event-6-image-2.jpg" alt="Data Science Bootcamp Sessions">''', '/content/event-images/event-6-thumbnail.jpg'),
        ('NLP Workshop', 'event-7-nlp-workshop', '2025-08-25', '''<p>The NLP Workshop will teach participants the basics of Natural Language Processing, enabling them to create tools for text analysis.</p><img src="/content/event-images/event-7-image-1.jpg" alt="NLP Workshop Image"><p>In this workshop, participants will explore techniques like text classification, named entity recognition, and sentiment analysis.</p><img src="/content/event-images/event-7-image-2.jpg" alt="NLP Workshop Participants">''', '/content/event-images/event-7-thumbnail.jpg'),
        ('Automation Fair', 'event-8-automation-fair', '2025-09-10', '''<p>The Automation Fair highlights the latest technologies in robotics and automation systems.</p><img src="/content/event-images/event-8-image-1.jpg" alt="Automation Fair Image"><p>Participants will discover automation solutions for various industries, including manufacturing, logistics, and healthcare.</p><img src="/content/event-images/event-8-image-2.jpg" alt="Automation Fair Exhibitors">''', '/content/event-images/event-8-thumbnail.jpg'),
        ('Ethics Panel', 'event-9-ethics-panel', '2025-09-25', '''<p>The Ethics Panel will discuss the ethical challenges and societal implications of AI technologies.</p><img src="/content/event-images/event-9-image-1.jpg" alt="Ethics Panel Image"><p>Industry experts will explore topics such as privacy, bias in AI algorithms, and the impact of AI on jobs.</p><img src="/content/event-images/event-9-image-2.jpg" alt="Ethics Panel Discussion">''', '/content/event-images/event-9-thumbnail.jpg'),
        ('Vision Tech Expo', 'event-10-vision-tech-expo', '2025-10-05', '''<p>The Vision Tech Expo focuses on the latest advancements in computer vision technology.</p><img src="/content/event-images/event-10-image-1.jpg" alt="Vision Tech Expo Image"><p>Attendees will learn about applications such as facial recognition, autonomous driving, and augmented reality.</p><img src="/content/event-images/event-10-image-2.jpg" alt="Vision Tech Expo Demos">''', '/content/event-images/event-10-thumbnail.jpg')
    ]
    cursor.executemany('INSERT INTO events (title, slug, event_date, content, thumbnail) VALUES (?, ?, ?, ?, ?);', events)

    # Insert projects 
    projects = [
        ('AI Chatbot', 'project-1-ai-chatbot', '2025-03-01', '''<p>This project demonstrates how to build an AI-powered chatbot that can communicate with users and respond to questions.</p><img src="/content/project-images/project-1-image-1.jpg" alt="AI Chatbot Image"><p>Using natural language processing, the chatbot can understand user queries and provide appropriate responses.</p>''', '/content/project-images/project-1-thumbnail.jpg'),
        ('Self-driving Car Prototype', 'project-2-self-driving-car-prototype', '2025-03-10', '''<p>This project aims to develop a prototype for a self-driving car using machine learning and computer vision techniques.</p><img src="/content/project-images/project-2-image-1.jpg" alt="Self-driving Car Prototype Image"><p>The prototype uses sensors and deep learning models to make autonomous driving decisions in real-time.</p>''', '/content/project-images/project-2-thumbnail.jpg'),
        ('Face Recognition System', 'project-3-face-recognition-system', '2025-03-20', '''<p>This project implements a face recognition system that can identify individuals in real-time using computer vision algorithms.</p><img src="/content/project-images/project-3-image-1.jpg" alt="Face Recognition System Image"><p>The system has potential applications in security, personal identification, and access control.</p>''', '/content/project-images/project-3-thumbnail.jpg'),
        ('NLP Summarizer', 'project-4-nlp-summarizer', '2025-03-30', '''<p>The NLP Summarizer project focuses on developing an algorithm to automatically summarize long texts using natural language processing techniques.</p><img src="/content/project-images/project-4-image-1.jpg" alt="NLP Summarizer Image"><p>The tool can be used to condense articles, papers, and other lengthy documents into key points.</p>''', '/content/project-images/project-4-thumbnail.jpg'),
        ('Healthcare Diagnosis AI', 'project-5-healthcare-diagnosis-ai', '2025-04-05', '''<p>This project uses AI to assist in diagnosing diseases from medical data, such as X-rays and patient records.</p><img src="/content/project-images/project-5-image-1.jpg" alt="Healthcare Diagnosis AI Image"><p>The system aims to improve the accuracy and speed of medical diagnoses, ultimately saving lives and reducing healthcare costs.</p>''', '/content/project-images/project-5-thumbnail.jpg'),
        ('Autonomous Drone', 'project-6-autonomous-drone', '2025-04-10', '''<p>The Autonomous Drone project focuses on building a drone that can navigate autonomously through GPS and computer vision technologies.</p><img src="/content/project-images/project-6-image-1.jpg" alt="Autonomous Drone Image"><p>These drones have applications in surveillance, mapping, and delivery services.</p>''', '/content/project-images/project-6-thumbnail.jpg'),
        ('AI Financial Advisor', 'project-7-ai-financial-advisor', '2025-04-15', '''<p>This project implements an AI-based financial advisor that helps individuals make informed decisions about investments and savings.</p><img src="/content/project-images/project-7-image-1.jpg" alt="AI Financial Advisor Image"><p>Using machine learning, the advisor suggests optimal financial strategies based on historical data and current market trends.</p>''', '/content/project-images/project-7-thumbnail.jpg'),
        ('Warehouse Robot', 'project-8-warehouse-robot', '2025-04-20', '''<p>The Warehouse Robot project aims to develop an autonomous robot capable of organizing and managing inventory in a warehouse.</p><img src="/content/project-images/project-8-image-1.jpg" alt="Warehouse Robot Image"><p>Equipped with sensors and AI, the robot can optimize warehouse operations and reduce human labor.</p>''', '/content/project-images/project-8-thumbnail.jpg'),
        ('Medical Imaging AI', 'project-9-medical-imaging-ai', '2025-04-25', '''<p>The Medical Imaging AI project applies machine learning to analyze medical images such as MRIs and CT scans.</p><img src="/content/project-images/project-9-image-1.jpg" alt="Medical Imaging AI Image"><p>This technology aims to detect diseases and abnormalities faster and more accurately than human radiologists.</p>''', '/content/project-images/project-9-thumbnail.jpg'),
        ('AI in Robotics', 'project-10-ai-in-robotics', '2025-04-30', '''<p>This project demonstrates the use of AI algorithms in controlling and optimizing robotic movements and interactions.</p><img src="/content/project-images/project-10-image-1.jpg" alt="AI in Robotics Image"><p>These robots are used in various industries, from manufacturing to healthcare, to improve efficiency and precision.</p>''', '/content/project-images/project-10-thumbnail.jpg')
    ]
    cursor.executemany('INSERT INTO projects (title, slug, date_posted, content, thumbnail) VALUES (?, ?, ?, ?, ?);', projects)

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
