from fastapi import FastAPI, UploadFile, File, HTTPException
import os

ALLOWED_TYPES = ["image/png", "image/jpeg", "application/pdf"]

MAX_SIZE_MB = 5

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Validate size — read file into memory
    file_content = await file.read()
    if len(file_content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB allowed)")
    
    
    filename = file.filename
    save_path = f"uploads/{filename}"

    # Save file
    with open(save_path, "wb") as f:
        f.write(file_content)

    return {"message": "File uploaded successfully", "path": save_path}
