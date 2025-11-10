# app/hybrid_search_array.py
from app.db import fetch_all
from app.llm import embed_text
import numpy as np

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    if vec1 is None or vec2 is None:
        return 0.0
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def vector_search_products(query_text: str, top_k=5):
    """Search products by array similarity"""
    query_embedding = embed_text(query_text)
    
    # Get all products with embeddings
    products = fetch_all("SELECT id, name, price, name_embedding FROM products WHERE name_embedding IS NOT NULL")
    
    # Calculate similarities
    results = []
    for product in products:
        similarity = cosine_similarity(query_embedding, product['name_embedding'])
        results.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'similarity': similarity
        })
    
    # Sort by similarity and return top_k
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]

def vector_search_customers(query_text: str, top_k=5):
    """Search customers by array similarity"""
    query_embedding = embed_text(query_text)
    
    # Get all orders with embeddings
    orders = fetch_all("SELECT id, customer_name, order_total, order_date, customer_embedding FROM orders WHERE customer_embedding IS NOT NULL")
    
    # Calculate similarities
    results = []
    for order in orders:
        similarity = cosine_similarity(query_embedding, order['customer_embedding'])
        results.append({
            'id': order['id'],
            'customer_name': order['customer_name'],
            'order_total': order['order_total'],
            'order_date': order['order_date'],
            'similarity': similarity
        })
    
    # Sort by similarity and return top_k
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]