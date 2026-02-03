from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pdf2docx import Converter
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "PDF to DOCX API is running"}

@app.post("/convert")
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
    start=0,
    end=None,
    keep_blank_chars=True,
    layout=True
)

    converter.close()

    # Return DOCX as download
    return FileResponse(
        path=docx_path,
        filename="converted.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
