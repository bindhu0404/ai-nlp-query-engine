from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import ingestion, query, schema

app = FastAPI(title="AI Query Engine - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(ingestion.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(schema.router, prefix="/api")

@app.get("/")
async def home():
    return {"message": "Backend is running 🚀"}
