# scripts/fix_database_with_vector.py
import psycopg2

DATABASE_URL = "postgresql://postgres:bhumika15@localhost:5432/demodb"

def fix_database():
    print("🔄 Fixing database structure with vector support...")
    
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        with conn.cursor() as cur:
            # Step 1: Ensure vector extension is installed
            print("1. Installing vector extension...")
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                print("   ✅ Vector extension installed")
            except Exception as e:
                print(f"   ❌ Vector extension failed: {e}")
                print("   🔄 Using array fallback...")
                use_vector = False
            else:
                use_vector = True
            
            # Step 2: Drop existing tables
            print("2. Cleaning up existing tables...")
            tables_to_drop = ['hello', 'helo', 'products', 'employees', 'orders', 'departments']
            for table in tables_to_drop:
                try:
                    cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    print(f"   ✅ Dropped {table}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {table}: {e}")
            
            # Step 3: Create tables with appropriate type
            print("3. Creating correct tables...")
            
            if use_vector:
                embedding_type = "vector(768)"
                print("   📊 Using VECTOR type for embeddings")
            else:
                embedding_type = "REAL[]"
                print("   📊 Using ARRAY type for embeddings (fallback)")
            
            tables_sql = [
                """
                CREATE TABLE departments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
                """,
                f"""
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    department_id INTEGER,
                    email VARCHAR(255),
                    salary DECIMAL(10,2),
                    name_embedding {embedding_type}
                )
                """,
                f"""
                CREATE TABLE products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    price DECIMAL(10,2),
                    name_embedding {embedding_type}
                )
                """,
                f"""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_name VARCHAR(100),
                    employee_id INTEGER,
                    order_total DECIMAL(10,2),
                    order_date DATE,
                    customer_embedding {embedding_type}
                )
                """
            ]
            
            for sql in tables_sql:
                cur.execute(sql)
            print("   ✅ Tables created")
            
            # Step 4: Insert sample data
            print("4. Inserting sample data...")
            
            # Departments
            departments = ['Engineering', 'HR', 'Sales', 'Support']
            for dept in departments:
                cur.execute("INSERT INTO departments (name) VALUES (%s)", (dept,))
            print("   ✅ Departments added")
            
            # Employees
            employees = [
                ('Alice Johnson', 1, 'alice.johnson@example.com', 7000.00),
                ('Bob Smith', 3, 'bob.smith@example.com', 5500.00),
                ('Carol Lee', 2, 'carol.lee@example.com', 6000.00),
                ('David Kim', 1, 'david.kim@example.com', 7200.00)
            ]
            for name, dept_id, email, salary in employees:
                cur.execute(
                    "INSERT INTO employees (name, department_id, email, salary) VALUES (%s, %s, %s, %s)",
                    (name, dept_id, email, salary)
                )
            print("   ✅ Employees added")
            
            # Products
            products = [
                ('Wireless Mouse MX200', 29.99),
                ('Mechanical Keyboard K3', 89.99),
                ('USB-C Charging Cable 1m', 9.99),
                ('Gaming Headset H7', 59.99)
            ]
            for name, price in products:
                cur.execute(
                    "INSERT INTO products (name, price) VALUES (%s, %s)",
                    (name, price)
                )
            print("   ✅ Products added")
            
            # Orders
            orders = [
                ('John Doe', 1, 119.98, '2025-10-03'),
                ('Mary Jane', 2, 29.99, '2025-10-10'),
                ('Acme Corp', 3, 289.90, '2025-09-28'),
                ('Foo Bar', 4, 59.99, '2025-09-15')
            ]
            for cust_name, emp_id, total, date in orders:
                cur.execute(
                    "INSERT INTO orders (customer_name, employee_id, order_total, order_date) VALUES (%s, %s, %s, %s)",
                    (cust_name, emp_id, total, date)
                )
            print("   ✅ Orders added")
            
            print(f"🎉 Database fixed successfully! Using: {'VECTOR' if use_vector else 'ARRAY'}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()