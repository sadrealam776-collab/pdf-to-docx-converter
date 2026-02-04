from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pdf2docx import Converter
import os
import uuid

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Serve index.html at homepage
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/convert")
if file.size and file.size > 5 * 1024 * 1024:
    return {"error": "PDF too large. Max 5MB allowed."}

async def convert_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    docx_path = os.path.join(OUTPUT_DIR, f"{file_id}.docx")

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Convert PDF to DOCX
    converter = Converter(pdf_path)
converter.convert(
    docx_path,
    keep_blank_chars=True
)
converter.close()

    # Return DOCX as download
    return FileResponse(
        path=docx_path,
        filename="converted.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


