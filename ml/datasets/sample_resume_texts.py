"""
Synthetic, fictional resume/job-description dataset for development and
testing of the matching engine. No real people's data is used.

Run `python generate_sample_data.py` (from ml/datasets/) to turn the text
below into actual .pdf files under ml/datasets/resumes/, so they can be
exercised through the real upload -> parse -> match pipeline.
"""

RESUMES = {
    "aarav_sharma_strong_backend_match.pdf": """Aarav Sharma
aarav.sharma@example.com | 9876500001

Summary
Backend engineer with 3 years of experience building scalable REST APIs.

Education
B.Tech Computer Science
National Institute of Technology
2021

Experience
Backend Developer
FinPay Technologies
Jan 2021 - Present
Built REST APIs using Java and Spring Boot
Designed PostgreSQL schemas for payment processing
Deployed services with Docker on AWS

Projects
Payment Processing API
A Spring Boot service handling payment authorization with PostgreSQL and REST API design

Banking Backend
Microservices based banking backend using Java, Spring Boot, Docker

Certifications
AWS Certified Developer Associate
Oracle Certified Java Programmer
""",
    "priya_iyer_medium_match.pdf": """Priya Iyer
priya.iyer@example.com | 9876500002

Summary
Full-stack developer with a mix of frontend and backend experience.

Education
B.Tech Information Technology
Anna University
2022

Experience
Software Engineer
WebNest Solutions
Jun 2022 - Present
Built REST APIs using Node.js and Express.js
Worked with MongoDB and PostgreSQL
Some exposure to Docker

Projects
E-commerce Platform
Node.js and React based e-commerce site with PostgreSQL

Certifications
Meta Front-End Developer Certificate
""",
    "rohan_das_weak_match.pdf": """Rohan Das
rohan.das@example.com | 9876500003

Summary
Recent graduate interested in data analysis roles.

Education
B.Sc Statistics
Delhi University
2024

Experience
Intern
DataWorks Analytics
Jan 2024 - Jun 2024
Assisted with Excel based reporting
Learned basics of Python

Projects
Sales Dashboard
An Excel and Python based sales reporting dashboard

Certifications
""",
    "sneha_reddy_missing_cloud_skills.pdf": """Sneha Reddy
sneha.reddy@example.com | 9876500004

Summary
Backend developer strong in Java and Spring Boot but limited cloud exposure.

Education
B.Tech Computer Science
Osmania University
2020

Experience
Backend Developer
CoreStack Systems
2020 - 2023
Built REST APIs using Java and Spring Boot
Worked extensively with PostgreSQL and MySQL

Projects
Inventory Management System
A Spring Boot and PostgreSQL based inventory tracker with REST APIs

Certifications
Spring Professional Certification
""",
    "karan_mehta_senior_experience.pdf": """Karan Mehta
karan.mehta@example.com | 9876500005

Summary
Senior backend engineer with 6 years of experience leading API teams.

Education
M.Tech Computer Science
IIT Roorkee
2018

Experience
Senior Backend Engineer
Zentro Cloud
2018 - 2024
Led a team building REST APIs with Java, Spring Boot
Migrated services to AWS with Docker and Kubernetes
Owned PostgreSQL schema design for core services

Projects
Order Management Platform
Large scale Spring Boot and PostgreSQL platform deployed on AWS with Docker

Certifications
AWS Certified Solutions Architect
Certified Kubernetes Administrator
""",
    "meera_nair_frontend_profile.pdf": """Meera Nair
meera.nair@example.com | 9876500006

Summary
Frontend developer specializing in React applications.

Education
B.Tech Computer Science
College of Engineering Trivandrum
2021

Experience
Frontend Developer
PixelCraft Studio
2021 - Present
Built responsive UIs using React and TypeScript
Integrated REST APIs from backend services
Used Tailwind CSS for styling

Projects
Dashboard UI Kit
A React and TypeScript component library with Tailwind CSS

Certifications
"""
    ,
    "vikram_singh_data_scientist.pdf": """Vikram Singh
vikram.singh@example.com | 9876500007

Summary
Data scientist with experience in machine learning and NLP.

Education
M.Sc Data Science
ISI Kolkata
2021

Experience
Data Scientist
InsightAI Labs
2021 - Present
Built machine learning models using Python and scikit-learn
Worked on NLP pipelines with spaCy
Used PostgreSQL for data storage

Projects
Resume Matching Prototype
A Python based semantic matching prototype using sentence embeddings

Certifications
TensorFlow Developer Certificate
"""
    ,
    "ananya_gupta_no_experience.pdf": """Ananya Gupta
ananya.gupta@example.com | 9876500008

Summary
Final year Computer Science student seeking a backend developer role.

Education
B.Tech Computer Science
VIT Vellore
2025

Experience

Projects
Library Management System
A Java and Spring Boot based library management system with PostgreSQL
Built REST APIs for book search and reservation

Certifications
Java Programming Certificate (Coursera)
""",
}
