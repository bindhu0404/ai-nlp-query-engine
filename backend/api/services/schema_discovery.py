# backend/api/services/schema_discovery.py
from sqlalchemy import inspect, text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()

class SchemaDiscovery:
    """
    Auto-discover tables, columns and simple FK relationships from a database connection.
    If connection_string is provided, use it; else accept an engine.
    """

    def __init__(self, connection_string: str = None, engine=None):
        self.connection_string = connection_string
        if engine:
            self.engine = engine
        else:
            if connection_string:
                self.engine = create_engine(connection_string, pool_size=5, max_overflow=10, future=True)
            else:
                # fallback to default engine from environment
                from database import get_engine
                self.engine = get_engine()

    def analyze_database(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        schema = {}
        for t in tables:
            try:
                cols = inspector.get_columns(t)
                fk = inspector.get_foreign_keys(t)
                pk = inspector.get_pk_constraint(t)
                schema[t] = {
                    "columns": [{ "name": c["name"], "type": str(c["type"]) } for c in cols],
                    "primary_key": pk.get("constrained_columns") if pk else [],
                    "foreign_keys": fk
                }
            except Exception:
                # skip inaccessible tables
                continue
        # add heuristic naming suggestions
        annotated = self._annotate_tables(schema)
        return annotated

    def _annotate_tables(self, schema):
        # heuristics: attempt to label tables like employees, departments etc.
        keywords = {
            "employee": ["employee", "employees", "emp", "staff", "personnel", "person"],
            "department": ["department", "departments", "dept", "division"],
            "documents": ["document", "documents", "resume", "resumes"],
            "salary": ["salary", "compensation", "pay", "annual_salary", "comp"]
        }
        annotated = {}
        for t, meta in schema.items():
            lower = t.lower()
            likely = []
            for k, vals in keywords.items():
                for v in vals:
                    if v in lower:
                        likely.append(k)
                        break
            # also check columns
            col_names = [c["name"].lower() for c in meta["columns"]]
            for k, vals in keywords.items():
                for v in vals:
                    if any(v in cn for cn in col_names):
                        if k not in likely:
                            likely.append(k)
            annotated[t] = {**meta, "likely": likely}
        return annotated

    def map_nl_to_schema(self, query: str, schema: dict):
        """
        Very basic mapping: returns candidate tables/columns for tokens.
        """
        tokens = [t.strip() for t in query.lower().split() if t.strip()]
        matches = {}
        for tname, meta in schema.items():
            score = 0
            col_names = [c["name"].lower() for c in meta["columns"]]
            for tok in tokens:
                if any(tok in c for c in col_names):
                    score += 2
                if tok in tname.lower():
                    score += 1
            if score > 0:
                matches[tname] = {"score": score, "columns": col_names}
        return matches
