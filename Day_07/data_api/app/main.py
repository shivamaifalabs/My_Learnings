from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import uuid

# adjust import path depending on folder structure
from processing import process_csv_file, stream_process_csv

app = FastAPI(title="Data Processing API")


# ---------- Utility: save uploaded file ----------
def save_uploaded_file(file: UploadFile, upload_dir: str = "uploads") -> str:
    os.makedirs(upload_dir, exist_ok=True)
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# ---------- Background processing task ----------
def background_process_csv(file_path: str):
    process_csv_file(file_path, outputs_folder="outputs")


# ---------- Endpoints ----------

@app.get("/")
def root():
    return {"message": "Data Processing API is running"}


# 1) CSV processing
@app.post("/process/csv")
async def process_csv_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    file_path = save_uploaded_file(file)
    result_paths = process_csv_file(file_path, outputs_folder="outputs")

    return {
        "message": "File processed successfully.",
        "cleaned_data": os.path.basename(result_paths["cleaned_data"]),
        "reports_folder": os.path.basename(result_paths["reports_folder"]),
        "plots_folder": os.path.basename(result_paths["plots_folder"]),
    }


# 2) Background processing
@app.post("/process/csv/background")
async def process_csv_background(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    file_path = save_uploaded_file(file)
    background_tasks.add_task(background_process_csv, file_path)

    return {"message": "File uploaded. Processing started in background."}


# 3) Stream processing (for very large CSVs)
@app.post("/process/csv/stream")
async def stream_csv_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    processed_path = stream_process_csv(file.file, outputs_folder="outputs")

    return {
        "message": "Large file processed in streaming mode.",
        "processed_file": os.path.basename(processed_path),
    }



# 4) Summary endpoint (updated to support NO-SALARY dataset)
@app.get("/summary/cleaned")
def summary_cleaned():
    cleaned_path = os.path.join("outputs", "cleaned_data.csv")
    if not os.path.exists(cleaned_path):
        return JSONResponse(
            status_code=404,
            content={"error": "No cleaned_data.csv found. Process a file first."},
        )

    import pandas as pd
    df = pd.read_csv(cleaned_path)

    summary = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": list(df.columns),
    }

    # add smart summaries based on available columns
    if "Department" in df.columns:
        summary["department_count"] = df["Department"].nunique()
    if "City" in df.columns:
        summary["city_count"] = df["City"].nunique()
    if "AgeGroup" in df.columns:
        summary["agegroup_count"] = df["AgeGroup"].nunique()

    return summary
