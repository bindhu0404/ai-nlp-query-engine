# AI Query Engine for Employee Data

## Overview

This project is a **Natural Language Query Engine** for employee databases and documents. It dynamically discovers database schemas, processes natural language queries, handles structured and unstructured data, and displays results via a React frontend.

Key features implemented:
- Database schema discovery
- Document ingestion (PDF, TXT, CSV, DOCX)
- Natural language query to SQL conversion
- Query caching and history
- Previous query auto-suggestions
- Responsive React frontend with TailwindCSS
- Performance metrics display (response time)
- Safe execution with error handling

> Note: Deployment is optional. The system can be run entirely locally.

---


---

## Setup Instructions

### Prerequisites

- Python 3.8+ (tested with 3.12)
- Node.js & npm
- PostgreSQL or Supabase/Postgres connection

---

### Backend Setup

1. Navigate to backend:

```bash
cd backend
```
2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file (based on .env.example):

```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
SUPABASE_URL=<your supabase url>
SUPABASE_KEY=<your supabase key>
HUGGINGFACE_API_KEY=<your huggingface key>
```

5. Start the backend server:

```bash
uvicorn app:app --reload --port 8000
```


## Backend endpoints:

POST /api/ingest/database → Connect & discover schema

POST /api/ingest/documents → Upload multiple documents

GET /api/ingest/status/{job_id} → Check document processing status

POST /api/query → Submit natural language query

GET /api/query/history → Get previous queries


## Features Implemented

Dynamic schema discovery from DB

Document ingestion with preview

Natural language query to SQL (dynamic, not hard-coded)

Query caching & history

Query auto-suggestions from previous queries

Responsive frontend with React & Tailwind

Error handling and feedback for user actions

Safe SQL execution