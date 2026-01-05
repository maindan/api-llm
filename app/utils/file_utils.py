import os
import uuid

UPLOAD_DIR = "uploads"

def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_file_name(original_name: str | None, mime_type: str | None) -> str:
    ext = ""

    if original_name and "." in original_name:
        ext = original_name.split(".")[-1]
    elif mime_type:
        if "jpeg" in mime_type:
            ext = "jpg"
        elif "png" in mime_type:
            ext = "png"
        elif "pdf" in mime_type:
            ext = "pdf"

    return f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())