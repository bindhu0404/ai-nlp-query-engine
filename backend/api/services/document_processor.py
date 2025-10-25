# backend/api/services/document_processor.py
import os
from pathlib import Path
from PyPDF2 import PdfReader
import csv
import json
import datetime

# Simple document storage in local JSON index: ./uploaded_docs/index.json
class DocumentProcessor:
    def __init__(self, upload_dir="./uploaded_docs"):
        self.upload_dir = upload_dir
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        self.index_file = os.path.join(self.upload_dir, "index.json")
        if not os.path.exists(self.index_file):
            with open(self.index_file, "w", encoding="utf8") as f:
                json.dump({"docs": []}, f)

    def process_document(self, path: str):
        text = self._extract_text(path)
        # store entry in index
        entry = {
            "id": Path(path).name,
            "path": path,
            "text": text[:4000],  # store truncated preview to keep index small
            "full_text_stored": False,
            "uploaded_at": datetime.datetime.utcnow().isoformat()
        }
        data = self._read_index()
        data["docs"].append(entry)
        self._write_index(data)
        return entry

    def _read_index(self):
        with open(self.index_file, "r", encoding="utf8") as f:
            return json.load(f)

    def _write_index(self, data):
        with open(self.index_file, "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _extract_text(self, path: str) -> str:
        path = str(path)
        lower = path.lower()
        try:
            if lower.endswith(".pdf"):
                return self._extract_pdf(path)
            if lower.endswith(".csv"):
                return self._extract_csv(path)
            if lower.endswith(".txt"):
                with open(path, "r", encoding="utf8", errors="ignore") as f:
                    return f.read()
            # docx optional fallback: try to import python-docx if available
            if lower.endswith(".docx"):
                try:
                    from docx import Document
                    doc = Document(path)
                    return "\n".join(p.text for p in doc.paragraphs)
                except Exception:
                    return ""
            return ""
        except Exception:
            return ""

    def _extract_pdf(self, path):
        try:
            reader = PdfReader(path)
            out = []
            for p in reader.pages:
                try:
                    out.append(p.extract_text() or "")
                except Exception:
                    continue
            return "\n".join(out)
        except Exception:
            return ""

    def _extract_csv(self, path):
        out = []
        try:
            with open(path, newline='', encoding='utf8', errors='ignore') as csvfile:
                snip = csvfile.read(20000)
                return snip
        except Exception:
            return ""
