from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from pdf2docx import Converter

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "API is running"}

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    docx_path = os.path.join(
        OUTPUT_DIR, file.filename.replace(".pdf", ".docx")
    )

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    converter = Converter(pdf_path)
    converter.convert(docx_path)
    converter.close()

    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(docx_path)
    )
