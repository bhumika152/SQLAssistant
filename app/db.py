# Database connection & helper functions
# app/db.py
import os
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from pgvector.psycopg2 import register_vector

from app.utils import DATABASE_URL

_conn = None

def get_conn():
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(DATABASE_URL)
        register_vector(_conn)  # register vector type with psycopg2
    return _conn

def fetch_all(query, params=None):
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params or ())
        rows = cur.fetchall()
    return rows

def execute(query, params=None):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        conn.commit()
