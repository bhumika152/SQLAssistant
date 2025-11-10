# 🧠 NLP-SQL Search Engine

A natural language to SQL query translation and retrieval system using PostgreSQL + pgvector + OpenAI embeddings, enabling users to query structured databases with human-like language.

# 📸 Demo Preview

<img width="1328" height="887" alt="image" src="https://github.com/user-attachments/assets/b2e9edd4-86e6-450d-b30c-c5495159c7db" />



# ⚙️ Tech Stack
Category	Tools / Libraries
Language	🐍 Python 3.10+
Database	🐘 PostgreSQL + pgvector extension
Containerization	🐳 Docker + docker-compose
ORM / DB Access	psycopg2
Embedding Model	Google gemini Embeddings 
App Structure	Modular folder hierarchy (db_init, scripts, src)


# 🧩 Project Structure
nlp-sql-search/
├─ docker-compose.yml
├─ db_init/
│  ├─ init-db.sql          # create tables + sample data
│  └─ create_pgvector.sql  # create pgvector extension
├─ scripts/
│  ├─ populate_embeddings.py
│  └─ seed_additional.py
├─ src/
│  ├─ main.py              # main app logic
│  ├─ nlp_to_sql.py        # convert natural language → SQL
│  └─ utils.py             # helpers, validation, logging
├─ .env                    # OpenAI key, DB creds
└─ README.md

# 🚀 Setup & Run
1️⃣ Clone the Repository
git clone https://github.com/bhumika152/SQLAssistant.git
cd nlp-sql-search

2️⃣ Environment Setup
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt


Add your API keys in .env:

OPENAI_API_KEY=your_api_key
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=demodb

🐳 Run with Docker
3️⃣  Database Initialization

-> Start PostgreSQL with pgvector
docker-compose up -d

-> Check if database is ready
docker-compose logs db

-> Verify pgvector extension
docker-compose exec db psql -U postgres -d demodb -c "SELECT * FROM pg_extension WHERE extname = 'vector';"

# 4. Run the Application

->Install Python dependencies
pip install -r requirements.txt

-> Launch Streamlit app
streamlit run app/streamlit_app.py

# 🧬 Embedding Population

After tables are created, populate embeddings:

python scripts/populate_embeddings.py


This script:

Reads text fields from DB

Generates vector embeddings via Google gemini

Stores them in the pgvector column

# ✨ Features
🤖 AI-Powered SQL Generation: Convert natural language to SQL using OpenAI GPT

🔍 Hybrid Vector Search: Combine traditional SQL with semantic vector search

🛡️ SQL Validation: Automatic SQL syntax and security validation

🎯 Smart Suggestions: Vector-based recommendations for products and customers

💫 Real-time Results: Instant query execution and visualization

🐳 Docker Ready: Complete containerized setup with pgvector


# 🧠 Methodology

Input Query → User enters natural language text

NLP Parsing → Preprocessing + intent extraction

SQL Generation → Convert to SQL using templates or model

Vector Retrieval → Search semantically similar entries via pgvector

Ranking & Result Display → Return the most relevant tuples


# 📊 Database Schema Example
Table	Columns
documents	id (PK), content, embedding (vector)
metadata	doc_id (FK), tags, timestamp
🧩 Example Query

Input:

“Show me all employees hired after 2022 with salary above 80k”

Generated SQL:

SELECT name, salary, hire_date 
FROM employees 
WHERE hire_date > '2022-01-01' AND salary > 80000;

# 🧱 References

PostgreSQL Documentation

pgvector Extension

Docker Official Docs

Google Gemini Embeddings Guide

LangChain Docs

# 🪪 License

This project is licensed under the MIT License – free to use and modify.

# 👩‍💻 Author

Bhumika Raheja
BTech, BML Munjal University
