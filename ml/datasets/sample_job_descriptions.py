"""
Synthetic job description dataset (3-5 roles) used to exercise strong /
medium / weak match scenarios against the sample resumes in
sample_resume_texts.py.
"""

JOB_DESCRIPTIONS = {
    "backend_developer.json": {
        "title": "Backend Developer",
        "description": """Backend Developer

We are looking for a Backend Developer to join our fintech platform team.

Required Skills:
Java, Spring Boot, REST API, PostgreSQL

Preferred Skills:
Docker, AWS

Minimum 2 years of experience required.
Bachelor's degree in Computer Science or related field preferred.

Responsibilities:
Design and build REST APIs
Own PostgreSQL schema design
Collaborate with frontend and DevOps teams
""",
    },
    "senior_backend_engineer.json": {
        "title": "Senior Backend Engineer",
        "description": """Senior Backend Engineer

Required Skills:
Java, Spring Boot, PostgreSQL, AWS, Docker, Kubernetes

Preferred Skills:
Terraform, CI/CD

Minimum 5 years of experience required.
Master's degree preferred.

Responsibilities:
Lead backend architecture decisions
Mentor junior engineers
Own cloud infrastructure on AWS
""",
    },
    "frontend_developer.json": {
        "title": "Frontend Developer",
        "description": """Frontend Developer

Required Skills:
React, TypeScript, REST API

Preferred Skills:
Tailwind CSS, Next.js

Minimum 1 years of experience required.

Responsibilities:
Build responsive user interfaces
Integrate with backend REST APIs
Collaborate with designers
""",
    },
    "data_scientist.json": {
        "title": "Data Scientist",
        "description": """Data Scientist

Required Skills:
Python, Machine Learning, scikit-learn, PostgreSQL

Preferred Skills:
Natural Language Processing, TensorFlow

Minimum 2 years of experience required.
Master's degree in Data Science, Statistics or related field preferred.

Responsibilities:
Build and evaluate machine learning models
Design NLP pipelines
Present insights to stakeholders
""",
    },
    "devops_engineer.json": {
        "title": "DevOps Engineer",
        "description": """DevOps Engineer

Required Skills:
Docker, Kubernetes, AWS, CI/CD

Preferred Skills:
Terraform, Jenkins

Minimum 2 years of experience required.

Responsibilities:
Manage CI/CD pipelines
Own container orchestration with Kubernetes
Maintain AWS cloud infrastructure
""",
    },
}
