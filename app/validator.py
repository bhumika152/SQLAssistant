# SQL validation & sanitizer
# app/validator.py
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

ALLOWED_TABLES = {"employees", "departments", "orders", "products"}
ALLOWED_VERBS = {"select"}

def is_select_only(sql_text: str) -> bool:
    try:
        parsed = sqlparse.parse(sql_text)
        if len(parsed) == 0:
            return False
        for stmt in parsed:
            # ensure the first token is a SELECT
            first_token = stmt.token_first(skip_cm=True)
            if first_token is None:
                return False
            if first_token.normalized.lower() not in ALLOWED_VERBS:
                return False
        return True
    except Exception:
        return False

def contains_forbidden(sql_text: str) -> bool:
    lowered = sql_text.lower()
    # Removed ";", "--", "/*", "*/" from forbidden list as they're common in valid SQL
    forbidden = ["insert ", "update ", "delete ", "drop ", "alter ", "create ", "grant ", "revoke "]
    return any(tok in lowered for tok in forbidden)

def extract_identifiers(stmt):
    # helper to extract table names from parsed tokens (basic)
    tables = set()
    for token in stmt.tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                tables.add(identifier.get_name())
        elif isinstance(token, Identifier):
            tables.add(token.get_name())
    return tables

def validate_sql(sql_text: str) -> tuple[bool, str]:
    if contains_forbidden(sql_text):
        return False, "Forbidden keywords detected (DDL/DML). Only SELECT queries allowed."
    if not is_select_only(sql_text):
        return False, "Only SELECT queries are allowed."
    
    # basic table whitelist check
    try:
        parsed = sqlparse.parse(sql_text)
        for stmt in parsed:
            # more flexible check: does any allowed table appear
            found = False
            s = stmt.value.lower()
            for t in ALLOWED_TABLES:
                # Check for table names in various contexts
                if (f" {t} " in s or 
                    f" {t}," in s or 
                    f" {t}." in s or
                    f"from {t}" in s or
                    f"join {t}" in s):
                    found = True
                    break
            if not found:
                # If query doesn't reference any of our tables, reject
                return False, f"Query doesn't reference allowed tables. Allowed: {ALLOWED_TABLES}"
        return True, "SQL appears valid."
    except Exception as e:
        return False, f"SQL parsing error: {e}"