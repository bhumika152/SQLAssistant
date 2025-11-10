-- SQL script to create tables + sample data
-- Enable pgvector (ankane image already has it, but safe)
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop tables if re-initializing (optional)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- Departments
CREATE TABLE departments (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

-- Employees
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  department_id INT REFERENCES departments(id),
  email VARCHAR(255),
  salary DECIMAL(10,2)
);

-- Orders
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(100),
  employee_id INT REFERENCES employees(id),
  order_total DECIMAL(10,2),
  order_date DATE
);

-- Products
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  price DECIMAL(10,2)
);

-- Add vector columns for searchable text fields
-- Use dimension 1536 as a default (adjust to your embedding model's dim)
ALTER TABLE products ADD COLUMN IF NOT EXISTS name_embedding vector(1536);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_embedding vector(1536);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS name_embedding vector(1536);

-- Sample data
INSERT INTO departments (name) VALUES ('Engineering'), ('HR'), ('Sales'), ('Support');

INSERT INTO employees (name, department_id, email, salary) VALUES
  ('Alice Johnson', 1, 'alice.johnson@example.com', 7000.00),
  ('Bob Smith', 3, 'bob.smith@example.com', 5500.00),
  ('Carol Lee', 2, 'carol.lee@example.com', 6000.00),
  ('David Kim', 1, 'david.kim@example.com', 7200.00);

INSERT INTO products (name, price) VALUES
  ('Wireless Mouse MX200', 29.99),
  ('Mechanical Keyboard K3', 89.99),
  ('USB-C Charging Cable 1m', 9.99),
  ('Gaming Headset H7', 59.99);

INSERT INTO orders (customer_name, employee_id, order_total, order_date) VALUES
  ('John Doe', 1, 119.98, '2025-10-03'),
  ('Mary Jane', 2, 29.99, '2025-10-10'),
  ('Acme Corp', 3, 289.90, '2025-09-28'),
  ('Foo Bar', 4, 59.99, '2025-09-15');
