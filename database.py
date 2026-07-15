import streamlit as st
from sqlalchemy import create_engine, text

# ✅ 100% Fixed Pooler URL: Properly formatted username and safely encoded '@' inside password
DATABASE_URL = "postgresql://postgres.rrexyeatjqouvdukubew:Ap%40bbf10060@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"

# Creating connection pool engine for cloud communication
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    with engine.connect() as conn:
        # Users Table Architecture
        conn.execute(text('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT)'''))
        
        # Expenses Ledger Table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS expenses (
                        id SERIAL PRIMARY KEY,
                        username TEXT,
                        type TEXT,
                        category TEXT,
                        description TEXT,
                        amount REAL,
                        date TEXT)'''))
        
        # Savings Milestones Table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS savings (
                        id SERIAL PRIMARY KEY,
                        username TEXT,
                        goal_name TEXT,
                        target_amount REAL,
                        current_amount REAL)'''))
        
        # Stock Monitors Table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS stocks (
                        id SERIAL PRIMARY KEY,
                        username TEXT,
                        ticker TEXT,
                        buy_price REAL)'''))
        
        # P2P Ledger Table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS p2p (
                        id SERIAL PRIMARY KEY,
                        username TEXT,
                        friend_name TEXT,
                        description TEXT,
                        amount REAL,
                        is_split TEXT)'''))
        conn.commit()

def run_query(query_str, params=(), fetch="none"):
    with engine.connect() as conn:
        param_dict = {}
        if params:
            if isinstance(params, tuple):
                for idx, val in enumerate(params):
                    param_dict[f"p{idx}"] = val
            elif isinstance(params, dict):
                param_dict = params

        processed_query = query_str
        for idx in range(10): 
            if "?" in processed_query:
                processed_query = processed_query.replace("?", f":p{idx}", 1)

        result = conn.execute(text(processed_query), param_dict)
        conn.commit()
        
        if fetch == "all":
            return result.fetchall()
        elif fetch == "one":
            return result.fetchone()
        return None

# Auto-initialize database tables directly inside Supabase Cloud
init_db()