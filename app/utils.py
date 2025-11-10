# Small utility functions (e.g., config loader)
# app/utils.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))
