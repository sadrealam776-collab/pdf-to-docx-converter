from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import time
from pdf2docx import Converter

# ---------------- APP ----------------
app = FastAPI(title="PDF to DOCX Converter")

# ---------------- FOLDERS ----------------
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- CLEANUP FUNCTION ----------------
def cleanup_old_files(folder, seconds=600):  # 10 minutes
    now = time.time()
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path) and now - os.path.getmtime(path) > seconds:
            os.remove(path)

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"status": "API is running"}

# ---------------- CONVERT ----------------
@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    # cleanup old files
    cleanup_old_files(UPLOAD_DIR)
    cleanup_old_files(OUTPUT_DIR)

    # file size limit (5MB)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        return JSONResponse(
            status_code=400,
            content={"error": "File too large. Max 5MB allowed."}
        )

    # paths
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    docx_path = os.path.join(
        OUTPUT_DIR, file.filename.replace(".pdf", ".docx")
    )

    # save pdf
    with open(pdf_path, "wb") as f:
        f.write(content)

    # convert
    try:
        converter = Converter(pdf_path)
        converter.convert(docx_path, keep_blank_chars=True)
        converter.close()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Conversion failed: {str(e)}"}
        )

    # return docx
    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(docx_path)
    )
