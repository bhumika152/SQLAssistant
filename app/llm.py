# app/llm.py
from app.utils import GOOGLE_API_KEY, EMBED_DIM
import os
import numpy as np

# Import Gemini
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("⚠️  google-generativeai not installed")

# Configure Gemini if available
if HAS_GENAI and GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("✅ Gemini API configured successfully")
    except Exception as e:
        print(f"❌ Gemini configuration error: {e}")
else:
    print("⚠️  Using mock implementations")

def embed_text(text: str):
    """
    Generate embeddings using Gemini's embedding model
    """
    if not text or not text.strip():
        return np.zeros(EMBED_DIM).tolist()
    
    if HAS_GENAI and GOOGLE_API_KEY:
        try:
            # Use the correct embedding model
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"❌ Error generating embedding with Gemini: {e}")
            return get_mock_embedding(text)
    else:
        return get_mock_embedding(text)

def get_mock_embedding(text):
    """Fallback mock embedding"""
    seed = hash(text) % (2**32)
    np.random.seed(seed)
    return np.random.randn(EMBED_DIM).tolist()

def text_to_sql(prompt: str, schema_description: str = "") -> str:
    """
    Convert natural language to SQL using Gemini
    """
    if HAS_GENAI and GOOGLE_API_KEY:
        try:
            return get_gemini_sql(prompt)
        except Exception as e:
            print(f"❌ Gemini SQL generation error: {e}")
            return get_mock_sql(prompt)
    else:
        print("⚠️  Using mock SQL generation")
        return get_mock_sql(prompt)

def get_gemini_sql(prompt: str) -> str:
    """Get SQL from Gemini with correct model names"""
    # Database schema
    SCHEMA_DESC = """
    PostgreSQL Database Schema:
    
    Tables:
    - departments(id SERIAL PRIMARY KEY, name VARCHAR(100))
    - employees(id SERIAL PRIMARY KEY, name VARCHAR(100), department_id INTEGER REFERENCES departments(id), email VARCHAR(255), salary DECIMAL(10,2))
    - products(id SERIAL PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2))
    - orders(id SERIAL PRIMARY KEY, customer_name VARCHAR(100), employee_id INTEGER REFERENCES employees(id), order_total DECIMAL(10,2), order_date DATE)
    
    Relationships:
    - employees.department_id -> departments.id
    - orders.employee_id -> employees.id
    
    Rules:
    - Only generate SELECT queries
    - No DML operations (INSERT, UPDATE, DELETE, DROP)
    - Use proper JOIN syntax
    - Return only SQL, no explanations
    """
    
    # Use the working models from your available list
    model_names = [
        "gemini-2.0-flash",           # Fast and reliable
        "gemini-2.0-flash-001",       # Stable version
        "gemini-flash-latest",        # Latest flash
        "gemini-pro-latest",          # Latest pro
        "gemini-2.5-flash",           # Newer model
    ]
    
    for model_name in model_names:
        try:
            print(f"🔧 Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            system_prompt = f"""Convert this natural language query to PostgreSQL SQL:

            {SCHEMA_DESC}

            Query: {prompt}

            Return ONLY the SQL query without any explanations, comments, or markdown formatting.
            Make sure the query starts with SELECT."""
            
            response = model.generate_content(system_prompt)
            sql_query = response.text.strip()
            
            # Clean the response
            sql_query = clean_sql_response(sql_query)
            
            print(f"✅ Generated SQL with {model_name}: {sql_query}")
            return sql_query
            
        except Exception as e:
            print(f"❌ Model {model_name} failed: {e}")
            continue
    
    # If all models fail, use mock
    print("❌ All Gemini models failed, using mock")
    return get_mock_sql(prompt)

def clean_sql_response(sql_query: str) -> str:
    """Clean and validate SQL response"""
    # Remove markdown code blocks
    if sql_query.startswith("```sql"):
        sql_query = sql_query[6:]
    elif sql_query.startswith("```"):
        sql_query = sql_query[3:]
    
    if sql_query.endswith("```"):
        sql_query = sql_query[:-3]
    
    sql_query = sql_query.strip()
    
    # Remove common prefixes and ensure it starts with SELECT
    if not sql_query.upper().startswith('SELECT'):
        # Try to find SELECT in the text
        select_pos = sql_query.upper().find('SELECT')
        if select_pos != -1:
            sql_query = sql_query[select_pos:]
        else:
            print(f"⚠️  No SELECT found in: {sql_query}")
            return get_mock_sql("fallback query")
    
    return sql_query

def get_mock_sql(prompt: str) -> str:
    """Fallback mock SQL generation"""
    query_lower = prompt.lower()
    
    # Enhanced pattern matching
    if any(word in query_lower for word in ["engineering", "engineer"]) and "salary" in query_lower:
        if any(term in query_lower for term in [">6000", "more than 6000", "over 6000", "above 6000"]):
            return "SELECT name, email, salary FROM employees WHERE department_id = 1 AND salary > 6000"
        elif "high" in query_lower or "highest" in query_lower:
            return "SELECT name, email, salary FROM employees WHERE department_id = 1 ORDER BY salary DESC LIMIT 3"
        else:
            return "SELECT name, email, salary FROM employees WHERE department_id = 1 ORDER BY salary DESC"
    
    elif "product" in query_lower and "price" in query_lower:
        if any(word in query_lower for word in ["expensive", "highest", "most expensive"]):
            return "SELECT name, price FROM products ORDER BY price DESC LIMIT 5"
        elif any(word in query_lower for word in ["cheap", "lowest", "least expensive"]):
            return "SELECT name, price FROM products ORDER BY price ASC LIMIT 5"
        else:
            return "SELECT name, price FROM products ORDER BY price"
    
    elif "order" in query_lower:
        if "recent" in query_lower:
            return "SELECT customer_name, order_total, order_date FROM orders ORDER BY order_date DESC LIMIT 10"
        elif "total" in query_lower:
            return "SELECT customer_name, order_total, order_date FROM orders ORDER BY order_total DESC LIMIT 10"
        else:
            return "SELECT customer_name, order_total, order_date FROM orders ORDER BY order_date DESC"
    
    elif "employee" in query_lower and "department" in query_lower:
        return "SELECT e.name, d.name as department, e.salary FROM employees e JOIN departments d ON e.department_id = d.id ORDER BY d.name, e.salary DESC"
    
    elif "department" in query_lower:
        return "SELECT id, name FROM departments ORDER BY name"
    
    elif "all employee" in query_lower:
        return "SELECT e.name, d.name as department, e.email, e.salary FROM employees e JOIN departments d ON e.department_id = d.id ORDER BY e.name"
    
    elif "all product" in query_lower:
        return "SELECT name, price FROM products ORDER BY name"
    
    else:
        return "SELECT e.name, d.name as department, e.salary FROM employees e JOIN departments d ON e.department_id = d.id LIMIT 10"