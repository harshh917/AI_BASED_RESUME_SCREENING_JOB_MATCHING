"""
Small curated skills taxonomy for a college project scope.

Not exhaustive — intentionally small and easy to extend. Maps every known
alias to a canonical name, and every canonical name to a category so the
skill_extractor can both normalize ("JS" -> "JavaScript") and bucket
("JavaScript" -> programming_languages).

Extending: add new entries to ALIASES (alias -> canonical) and make sure
the canonical name has a category in CATEGORY_OF (or it falls into "other").
"""

CANONICAL_SKILLS = {
    # programming_languages
    "Python": "programming_languages",
    "JavaScript": "programming_languages",
    "TypeScript": "programming_languages",
    "Java": "programming_languages",
    "C++": "programming_languages",
    "C": "programming_languages",
    "C#": "programming_languages",
    "Go": "programming_languages",
    "Rust": "programming_languages",
    "PHP": "programming_languages",
    "Ruby": "programming_languages",
    "Kotlin": "programming_languages",
    "Swift": "programming_languages",
    "R": "programming_languages",
    "SQL": "programming_languages",
    # frameworks
    "React": "frameworks",
    "Angular": "frameworks",
    "Vue.js": "frameworks",
    "Node.js": "frameworks",
    "Express.js": "frameworks",
    "Django": "frameworks",
    "Flask": "frameworks",
    "FastAPI": "frameworks",
    "Spring Boot": "frameworks",
    "ASP.NET": "frameworks",
    "Next.js": "frameworks",
    "TensorFlow": "frameworks",
    "PyTorch": "frameworks",
    "scikit-learn": "frameworks",
    "Pandas": "frameworks",
    "NumPy": "frameworks",
    # databases
    "PostgreSQL": "databases",
    "MySQL": "databases",
    "MongoDB": "databases",
    "SQLite": "databases",
    "Redis": "databases",
    "Oracle DB": "databases",
    "Cassandra": "databases",
    "Elasticsearch": "databases",
    # cloud
    "AWS": "cloud",
    "Azure": "cloud",
    "Google Cloud Platform": "cloud",
    "Firebase": "cloud",
    "Heroku": "cloud",
    # tools
    "Docker": "tools",
    "Kubernetes": "tools",
    "Git": "tools",
    "Jenkins": "tools",
    "GitHub Actions": "tools",
    "Terraform": "tools",
    "Postman": "tools",
    "Linux": "tools",
    "Nginx": "tools",
    # other technical
    "REST API": "other",
    "GraphQL": "other",
    "Microservices": "other",
    "CI/CD": "other",
    "Machine Learning": "other",
    "Deep Learning": "other",
    "Natural Language Processing": "other",
    "Data Structures and Algorithms": "other",
}

# alias (lowercased match key) -> canonical name
ALIASES = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "reactjs": "React",
    "react.js": "React",
    "react": "React",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    "express": "Express.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud Platform",
    "google cloud": "Google Cloud Platform",
    "google cloud platform": "Google Cloud Platform",
    "azure": "Azure",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "git": "Git",
    "github": "Git",
    "spring boot": "Spring Boot",
    "springboot": "Spring Boot",
    "spring": "Spring Boot",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "asp.net": "ASP.NET",
    "dotnet": "ASP.NET",
    ".net": "ASP.NET",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "rest": "REST API",
    "rest api": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "graphql": "GraphQL",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "dsa": "Data Structures and Algorithms",
    "data structures and algorithms": "Data Structures and Algorithms",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "php": "PHP",
    "ruby": "Ruby",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "sql": "SQL",
    "linux": "Linux",
    "nginx": "Nginx",
    "terraform": "Terraform",
    "jenkins": "Jenkins",
    "postman": "Postman",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "cassandra": "Cassandra",
    "firebase": "Firebase",
    "heroku": "Heroku",
    "microservices": "Microservices",
    "next.js": "Next.js",
    "nextjs": "Next.js",
}


def normalize_skill(raw: str) -> str:
    """Return the canonical form of a skill string, or a title-cased fallback."""
    key = raw.strip().lower()
    if key in ALIASES:
        return ALIASES[key]
    if raw.strip() in CANONICAL_SKILLS:
        return raw.strip()
    return raw.strip()


def category_of(canonical_skill: str) -> str:
    return CANONICAL_SKILLS.get(canonical_skill, "other")
