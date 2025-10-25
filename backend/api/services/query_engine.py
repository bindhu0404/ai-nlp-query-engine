# backend/api/services/query_engine.py
import time
import pandas as pd
from sqlalchemy import text, inspect
from database import get_engine
from collections import deque

class QueryEngine:
    def __init__(self, cache_size=100, cache_ttl=300):
        self.engine = get_engine()
        self.cache = {}  # query -> {"results": ..., "generated_sql": ..., "timestamp": ...}
        self.cache_ttl = cache_ttl  # seconds
        self.history = deque(maxlen=cache_size)  # store last N queries

    def process_query(self, user_query: str):
        start = time.time()

        # --- Check cache first ---
        cache_entry = self.cache.get(user_query)
        if cache_entry:
            age = time.time() - cache_entry["timestamp"]
            if age <= self.cache_ttl:
                return {
                    "results": cache_entry["results"],
                    "generated_sql": cache_entry["generated_sql"],
                    "response_time": round(time.time() - start, 2),
                    "cache_hit": True
                }
            else:
                # expired
                del self.cache[user_query]

        insp = inspect(self.engine)
        schema = {t: [c["name"] for c in insp.get_columns(t)] for t in insp.get_table_names()}

        # Generate SQL
        sql_query = self.english_to_sql(user_query, schema)
        if not sql_query:
            return {
                "error": "Could not interpret your query. Try rephrasing.",
                "generated_sql": None,
                "response_time": round(time.time() - start, 2),
                "cache_hit": False
            }

        # Execute SQL
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql_query(text(sql_query), conn).to_dict(orient="records")
        except Exception as e:
            return {
                "error": str(e),
                "generated_sql": sql_query,
                "response_time": round(time.time() - start, 2),
                "cache_hit": False
            }

        # Store in cache & history
        self.cache[user_query] = {
            "results": result,
            "generated_sql": sql_query,
            "timestamp": time.time()
        }
        self.history.append({
            "query": user_query,
            "generated_sql": sql_query,
            "time": round(time.time() - start, 2)
        })

        return {
            "results": result,
            "generated_sql": sql_query,
            "response_time": round(time.time() - start, 2),
            "cache_hit": False
        }

    def get_history(self):
        """Return list of past queries"""
        return list(self.history)

    # --- keep your existing English-to-SQL logic ---
    def english_to_sql(self, query, schema):
        q = query.lower()

        # List employees
        if "employee" in q and ("all" in q or "list" in q):
            if "engineering" in q:
                if "above" in q or "greater" in q:
                    amount = ''.join([c for c in q if c.isdigit()])
                    return f"""
                        SELECT e.*, d.dept_name, d.manager 
                        FROM employees e
                        JOIN departments d ON e.department_id = d.dept_id
                        WHERE d.dept_name ILIKE '%engineering%' 
                        AND e.annual_salary > {amount or 0};
                    """
                return """
                    SELECT e.*, d.dept_name, d.manager 
                    FROM employees e
                    JOIN departments d ON e.department_id = d.dept_id
                    WHERE d.dept_name ILIKE '%engineering%';
                """
            return "SELECT * FROM employees;"

        # Salary-based query
        if "salary" in q and ("above" in q or "greater" in q):
            amount = ''.join([c for c in q if c.isdigit()])
            return f"SELECT * FROM employees WHERE annual_salary > {amount or 0};"

        # Department listing
        if "department" in q and ("all" in q or "list" in q):
            return "SELECT * FROM departments;"

        # Managers
        if "manager" in q or "managed by" in q:
            return """
                SELECT e.full_name, e.position, d.dept_name
                FROM employees e
                JOIN departments d ON e.department_id = d.dept_id
                WHERE e.position ILIKE '%manager%';
            """

        # Hires this year
        if "hired this year" in q or "joined this year" in q:
            return """
                SELECT * FROM employees
                WHERE EXTRACT(YEAR FROM join_date) = EXTRACT(YEAR FROM CURRENT_DATE);
            """

        # Default fallback
        return None
