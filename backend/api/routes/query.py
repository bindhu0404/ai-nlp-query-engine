# backend/api/routes/query.py
from fastapi import APIRouter
from api.services.query_engine import QueryEngine

router = APIRouter()

# Single persistent engine for caching & history
_engine_singleton = QueryEngine()

@router.post("/query")
async def process_query(req: dict):
    query = req.get("query")
    if not query:
        return {"error": "No query provided"}
    return _engine_singleton.process_query(query)

@router.get("/query/history")
async def query_history():
    return {"history": _engine_singleton.get_history()}
