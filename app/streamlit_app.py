
# # app/streamlit_app.py
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import streamlit as st
# import pandas as pd
# from app.llm import text_to_sql
# from app.validator import validate_sql
# from app.db import fetch_all
# from app.hybrid_search import vector_search_products, vector_search_customers
# from app.utils import EMBED_DIM

# # DEBUG: Print validator info
# print("🔄 Validator module reloaded - checking version...")
# try:
#     from app.validator import contains_forbidden
#     test_sql = "SELECT e.name FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Engineering' AND e.salary > 2000"
#     test_result = contains_forbidden(test_sql)
#     print(f"🔧 Validator test result: {test_result}")
#     if test_result:
#         print("❌ Validator is still blocking good SQL!")
#     else:
#         print("✅ Validator is working correctly!")
# except Exception as e:
#     print(f"❌ Validator error: {e}")

# # Provide a short schema description for the LLM
# SCHEMA_DESC = """
# Tables:
# - departments(id, name)
# - employees(id, name, department_id, email, salary)
# - products(id, name, price, name_embedding)
# - orders(id, customer_name, employee_id, order_total, order_date, customer_embedding)
# Relationships:
# employees.department_id -> departments.id
# orders.employee_id -> employees.id
# """

# st.set_page_config(page_title="NL → SQL Search (Postgres + pgvector)", layout="wide")

# st.title("Natural Language Search Interface — PostgreSQL + pgvector")

# with st.sidebar:
#     st.header("Settings")
#     use_hybrid = st.checkbox("Enable hybrid search (vector + SQL)", value=True)
#     show_sql = st.checkbox("Show generated SQL before executing", value=True)
#     top_k = st.number_input("Hybrid search top K", value=5, min_value=1, max_value=50)
    
#     # Add debug info in sidebar
#     st.header("🔧 Debug Info")
#     if st.button("Force Restart Validator"):
#         st.cache_data.clear()
#         st.success("Cache cleared - please refresh browser")

# query = st.text_input("Ask a question about employees/products/orders (e.g., 'Which employees in engineering earn > 6000?')", "")

# col1, col2 = st.columns([3,1])
# with col2:
#     if st.button("Search"):
#         if not query.strip():
#             st.warning("Please enter a query.")
#         else:
#             # Generate SQL from NL
#             generated_sql = text_to_sql(query, SCHEMA_DESC)
#             st.session_state['generated_sql'] = generated_sql
            
#             # DEBUG: Show what SQL we're validating
#             st.write("🔧 Debug - SQL to validate:")
#             st.code(repr(generated_sql))
            
#             valid, message = validate_sql(generated_sql)
            
#             # DEBUG: Show validation details
#             st.write(f"🔧 Validation result: {valid}")
#             st.write(f"🔧 Validation message: {message}")
            
#             if not valid:
#                 st.error("SQL validation failed: " + message)
#                 st.stop()

#             if show_sql:
#                 st.subheader("Generated SQL")
#                 st.code(generated_sql, language="sql")

#             try:
#                 # If hybrid search enabled, first run vector search to surface relevant rows (optional)
#                 results = []
#                 if use_hybrid:
#                     st.info("Performing hybrid vector retrieval...")
#                     # Example: if query includes 'product' or 'price', run product vector search
#                     product_hits = vector_search_products(query, top_k=top_k)
#                     customer_hits = vector_search_customers(query, top_k=top_k)
#                     # Show candidates
#                     st.subheader("Vector candidates (products)")
#                     st.table(pd.DataFrame(product_hits))

#                     st.subheader("Vector candidates (orders/customers)")
#                     st.table(pd.DataFrame(customer_hits))

#                 # Execute validated SQL
#                 rows = fetch_all(generated_sql)
#                 df = pd.DataFrame(rows)
#                 if df.empty:
#                     st.warning("No results from SQL execution.")
#                 else:
#                     st.subheader("Query Results")
#                     st.dataframe(df)
#             except Exception as e:
#                 st.error(f"Query execution error: {e}")

# Main Streamlit UI entry point
# app/streamlit_app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from app.llm import text_to_sql
from app.validator import validate_sql
from app.db import fetch_all
from app.hybrid_search import vector_search_products, vector_search_customers
from app.utils import EMBED_DIM

# DEBUG: Print validator info
print("🔄 Validator module reloaded - checking version...")
try:
    from app.validator import contains_forbidden
    test_sql = "SELECT e.name FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Engineering' AND e.salary > 2000"
    test_result = contains_forbidden(test_sql)
    print(f"🔧 Validator test result: {test_result}")
    if test_result:
        print("❌ Validator is still blocking good SQL!")
    else:
        print("✅ Validator is working correctly!")
except Exception as e:
    print(f"❌ Validator error: {e}")

# Provide a short schema description for the LLM
SCHEMA_DESC = """
Tables:
- departments(id, name)
- employees(id, name, department_id, email, salary)
- products(id, name, price, name_embedding)
- orders(id, customer_name, employee_id, order_total, order_date, customer_embedding)
Relationships:
employees.department_id -> departments.id
orders.employee_id -> employees.id
"""

st.set_page_config(page_title="NL → SQL Search (Postgres + pgvector)", layout="wide")

# Custom CSS for full-width centered layout
st.markdown("""
<style>
    .main .block-container {
        max-width: 95%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .full-width {
        width: 100%;
        margin: 0 auto;
    }
    
    .centered-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #0d6efd;
    }
    
    .debug-section {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .result-section {
        background-color: #d1e7dd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #198754;
    }
    
    .sql-code {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        margin: 0.5rem 0;
    }
    
    .stButton button {
        width: 100%;
        background-color: #0d6efd;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #0b5ed7;
    }
</style>
""", unsafe_allow_html=True)

st.title("Natural Language Search Interface — PostgreSQL + pgvector")

with st.sidebar:
    st.header("Settings")
    use_hybrid = st.checkbox("Enable hybrid search (vector + SQL)", value=True)
    show_sql = st.checkbox("Show generated SQL before executing", value=True)
    top_k = st.number_input("Hybrid search top K", value=5, min_value=1, max_value=50)
    
    # Add debug info in sidebar
    st.header("🔧 Debug Info")
    if st.button("Force Restart Validator"):
        st.cache_data.clear()
        st.success("Cache cleared - please refresh browser")

# Main content area - full width
st.markdown('<div class="full-width">', unsafe_allow_html=True)

# Query input - full width
query = st.text_input(
    "Ask a question about employees/products/orders (e.g., 'Which employees in engineering earn > 6000?')", 
    "",
    key="main_query"
)

# Search button - full width
if st.button("Search", key="main_search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        # Generate SQL from NL
        generated_sql = text_to_sql(query, SCHEMA_DESC)
        st.session_state['generated_sql'] = generated_sql
        
        # Debug section - full width
        with st.container():
            st.markdown('<div class="debug-section">', unsafe_allow_html=True)
            st.subheader("🔧 Debug Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**SQL to validate:**")
                st.code(generated_sql, language="sql")
            
            with col2:
                valid, message = validate_sql(generated_sql)
                st.write(f"**Validation result:** {'✅ Valid' if valid else '❌ Invalid'}")
                st.write(f"**Validation message:** {message}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not valid:
            st.error("SQL validation failed: " + message)
        else:
            # Generated SQL section - full width
            if show_sql:
                with st.container():
                    st.markdown('<div class="centered-section">', unsafe_allow_html=True)
                    st.subheader("Generated SQL")
                    st.code(generated_sql, language="sql")
                    st.markdown('</div>', unsafe_allow_html=True)

            try:
                # Hybrid search section - full width
                if use_hybrid:
                    with st.container():
                        st.markdown('<div class="centered-section">', unsafe_allow_html=True)
                        st.info("Performing hybrid vector retrieval...")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            product_hits = vector_search_products(query, top_k=top_k)
                            st.subheader("Vector candidates (products)")
                            if product_hits:
                                st.table(pd.DataFrame(product_hits))
                            else:
                                st.write("No product results found")
                        
                        with col2:
                            customer_hits = vector_search_customers(query, top_k=top_k)
                            st.subheader("Vector candidates (orders/customers)")
                            if customer_hits:
                                st.table(pd.DataFrame(customer_hits))
                            else:
                                st.write("No customer results found")
                        
                        st.markdown('</div>', unsafe_allow_html=True)

                # Main results section - full width
                with st.container():
                    st.markdown('<div class="result-section">', unsafe_allow_html=True)
                    
                    # Execute validated SQL
                    rows = fetch_all(generated_sql)
                    df = pd.DataFrame(rows)
                    
                    if df.empty:
                        st.warning("No results from SQL execution.")
                    else:
                        st.subheader("Query Results")
                        st.dataframe(df, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Query execution error: {e}")

st.markdown('</div>', unsafe_allow_html=True)