# backend/api/routes/schema.py
from fastapi import APIRouter, HTTPException
from api.services.schema_discovery import SchemaDiscovery
from database import get_engine

router = APIRouter()

@router.get("/api/schema")
def get_schema():
    try:
        engine = get_engine()
        sd = SchemaDiscovery(engine=engine)
        schema = sd.analyze_database()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# register with app by importing module
from fastapi import FastAPI
app = FastAPI.__module__  # silence linter (not used)
