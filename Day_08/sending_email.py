from fastapi import FastAPI, BackgroundTasks,UploadFile, File
from pydantic import EmailStr
import smtplib

app = FastAPI()

def send_email_smtp(to_email: str):
    sender = "my_email@gmail.com"
    password = "your_app_password"
    subject = "Welcome"
    body = "Thank you for registering!"

    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, to_email, msg)

@app.post("/register")
async def register(email: EmailStr, tasks: BackgroundTasks):
    tasks.add_task(send_email_smtp, email)
    return {"message": "Registered. Welcome email will be sent."}



# File- Uploading:---
def process_file(path: str):
    print(f"Processing file: {path}")

@app.post("/upload")
async def upload(file: UploadFile = File(...), tasks: BackgroundTasks = None):
    file_path = f"uploads/{file.filename}"
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Process file in background
    tasks.add_task(process_file, file_path)

    return {"message": "File uploaded. Background processing started."}