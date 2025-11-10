# # # Script to compute embeddings for text fields
# # # scripts/populate_embeddings.py

# # import sys
# # import os

# # # Add the project root to Python path
# # sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# # import psycopg2
# # from app.utils import DATABASE_URL
# # from app.llm import embed_text
# # from pgvector.psycopg2 import register_vector

# # conn = psycopg2.connect(DATABASE_URL)
# # register_vector(conn)

# # def update_products():
# #     with conn.cursor() as cur:
# #         cur.execute("SELECT id, name FROM products WHERE name_embedding IS NULL OR name_embedding = ''")
# #         rows = cur.fetchall()
# #         for id_, name in rows:
# #             emb = embed_text(name)
# #             cur.execute("UPDATE products SET name_embedding = %s WHERE id = %s", (emb, id_))
# #     conn.commit()

# # def update_orders():
# #     with conn.cursor() as cur:
# #         cur.execute("SELECT id, customer_name FROM orders WHERE customer_embedding IS NULL OR customer_embedding = ''")
# #         rows = cur.fetchall()
# #         for id_, cust in rows:
# #             emb = embed_text(cust)
# #             cur.execute("UPDATE orders SET customer_embedding = %s WHERE id = %s", (emb, id_))
# #     conn.commit()

# # def update_employees():
# #     with conn.cursor() as cur:
# #         cur.execute("SELECT id, name FROM employees WHERE name_embedding IS NULL OR name_embedding = ''")
# #         rows = cur.fetchall()
# #         for id_, name in rows:
# #             emb = embed_text(name)
# #             cur.execute("UPDATE employees SET name_embedding = %s WHERE id = %s", (emb, id_))
# #     conn.commit()

# # if __name__ == "__main__":
# #     update_products()
# #     update_orders()
# #     update_employees()
# #     print("Embeddings populated.")
# # scripts/populate_embeddings_fixed.py
# import sys
# import os
# import psycopg2
# import numpy as np

# # Add the project root to Python path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# DATABASE_URL = "postgresql://postgres:bhumika15@localhost:5432/demodb"

# def get_connection():
#     """Get database connection and ensure vector extension is enabled"""
#     conn = psycopg2.connect(DATABASE_URL)
    
#     # Enable vector extension if not already enabled
#     with conn.cursor() as cur:
#         try:
#             cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
#             conn.commit()
#             print("✅ Vector extension enabled")
#         except Exception as e:
#             print(f"⚠️  Could not enable vector extension: {e}")
    
#     return conn

# def embed_text(text):
#     """Mock embedding function"""
#     if not text or not text.strip():
#         return np.zeros(768).tolist()
#     seed = hash(text) % (2**32)
#     np.random.seed(seed)
#     return np.random.randn(768).tolist()

# def ensure_vector_columns():
#     """Ensure vector columns exist in tables"""
#     conn = get_connection()
    
#     with conn.cursor() as cur:
#         # Check and add vector columns if they don't exist
#         try:
#             # Products table
#             cur.execute("""
#                 DO $$ 
#                 BEGIN 
#                     IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
#                                   WHERE table_name='products' AND column_name='name_embedding') THEN
#                         ALTER TABLE products ADD COLUMN name_embedding vector(768);
#                     END IF;
#                 END $$;
#             """)
            
#             # Orders table  
#             cur.execute("""
#                 DO $$ 
#                 BEGIN 
#                     IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
#                                   WHERE table_name='orders' AND column_name='customer_embedding') THEN
#                         ALTER TABLE orders ADD COLUMN customer_embedding vector(768);
#                     END IF;
#                 END $$;
#             """)
            
#             # Employees table
#             cur.execute("""
#                 DO $$ 
#                 BEGIN 
#                     IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
#                                   WHERE table_name='employees' AND column_name='name_embedding') THEN
#                         ALTER TABLE employees ADD COLUMN name_embedding vector(768);
#                     END IF;
#                 END $$;
#             """)
            
#             conn.commit()
#             print("✅ Vector columns verified")
            
#         except Exception as e:
#             print(f"⚠️  Error ensuring vector columns: {e}")
    
#     conn.close()

# def update_products():
#     print("🔄 Updating product embeddings...")
#     conn = get_connection()
    
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, name FROM products WHERE name_embedding IS NULL")
#         rows = cur.fetchall()
        
#         for id_, name in rows:
#             print(f"  Processing product: {name}")
#             emb = embed_text(name)
#             cur.execute("UPDATE products SET name_embedding = %s WHERE id = %s", (emb, id_))
            
#     conn.commit()
#     conn.close()
#     print(f"✅ Updated {len(rows)} products")

# def update_orders():
#     print("🔄 Updating order embeddings...")
#     conn = get_connection()
    
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, customer_name FROM orders WHERE customer_embedding IS NULL")
#         rows = cur.fetchall()
        
#         for id_, cust in rows:
#             print(f"  Processing order for: {cust}")
#             emb = embed_text(cust)
#             cur.execute("UPDATE orders SET customer_embedding = %s WHERE id = %s", (emb, id_))
            
#     conn.commit()
#     conn.close()
#     print(f"✅ Updated {len(rows)} orders")

# def update_employees():
#     print("🔄 Updating employee embeddings...")
#     conn = get_connection()
    
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, name FROM employees WHERE name_embedding IS NULL")
#         rows = cur.fetchall()
        
#         for id_, name in rows:
#             print(f"  Processing employee: {name}")
#             emb = embed_text(name)
#             cur.execute("UPDATE employees SET name_embedding = %s WHERE id = %s", (emb, id_))
            
#     conn.commit()
#     conn.close()
#     print(f"✅ Updated {len(rows)} employees")

# def create_indexes():
#     """Create vector indexes for faster search"""
#     print("🔄 Creating vector indexes...")
#     conn = get_connection()
    
#     with conn.cursor() as cur:
#         try:
#             cur.execute("""
#                 CREATE INDEX IF NOT EXISTS products_name_embedding_idx 
#                 ON products USING ivfflat (name_embedding vector_cosine_ops)
#             """)
#             cur.execute("""
#                 CREATE INDEX IF NOT EXISTS orders_customer_embedding_idx 
#                 ON orders USING ivfflat (customer_embedding vector_cosine_ops)
#             """)
#             cur.execute("""
#                 CREATE INDEX IF NOT EXISTS employees_name_embedding_idx 
#                 ON employees USING ivfflat (name_embedding vector_cosine_ops)
#             """)
#             conn.commit()
#             print("✅ Vector indexes created")
#         except Exception as e:
#             print(f"⚠️  Could not create indexes: {e}")
    
#     conn.close()

# if __name__ == "__main__":
#     try:
#         print("🚀 Starting embedding population...")
        
#         # Step 1: Ensure vector extension and columns exist
#         ensure_vector_columns()
        
#         # Step 2: Populate embeddings
#         update_products()
#         update_orders()
#         update_employees()
        
#         # Step 3: Create indexes
#         create_indexes()
        
#         print("🎉 All embeddings populated successfully!")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         print("Make sure the database is running: docker-compose up -d")
# scripts/populate_embeddings_array.py
import psycopg2
import numpy as np

DATABASE_URL = "postgresql://postgres:bhumika15@localhost:5432/demodb"

def get_connection():
    """Get database connection"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.rollback()  # Clean transaction state
    return conn

def embed_text(text):
    """Mock embedding function - returns Python list for arrays"""
    if not text or not text.strip():
        return np.zeros(768).tolist()
    seed = hash(text) % (2**32)
    np.random.seed(seed)
    return np.random.randn(768).tolist()

def populate_embeddings():
    print("🚀 Starting embedding population with ARRAYS...")
    
    try:
        # Products
        print("🔄 Updating product embeddings...")
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM products WHERE name_embedding IS NULL")
            rows = cur.fetchall()
            
            for id_, name in rows:
                print(f"  Processing: {name}")
                emb = embed_text(name)
                cur.execute("UPDATE products SET name_embedding = %s WHERE id = %s", (emb, id_))
            
            conn.commit()
            print(f"✅ Updated {len(rows)} products")
        conn.close()
        
        # Orders
        print("🔄 Updating order embeddings...")
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, customer_name FROM orders WHERE customer_embedding IS NULL")
            rows = cur.fetchall()
            
            for id_, cust in rows:
                print(f"  Processing: {cust}")
                emb = embed_text(cust)
                cur.execute("UPDATE orders SET customer_embedding = %s WHERE id = %s", (emb, id_))
            
            conn.commit()
            print(f"✅ Updated {len(rows)} orders")
        conn.close()
        
        # Employees
        print("🔄 Updating employee embeddings...")
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM employees WHERE name_embedding IS NULL")
            rows = cur.fetchall()
            
            for id_, name in rows:
                print(f"  Processing: {name}")
                emb = embed_text(name)
                cur.execute("UPDATE employees SET name_embedding = %s WHERE id = %s", (emb, id_))
            
            conn.commit()
            print(f"✅ Updated {len(rows)} employees")
        conn.close()
        
        print("🎉 All embeddings populated successfully with ARRAYS!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_embeddings()