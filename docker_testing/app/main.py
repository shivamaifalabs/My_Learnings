from fastapi import FastAPI


app= FastAPI(title='Testing this thorugh Docker!')

@app.get('/')
def root():
    return {"status": "ok", "message": "Your API's is working Good!"}

# Liveness check
@app.get("/health")
def health():
    return {"status": "alive"}

# Readiness check
@app.get("/ready")
def readiness():
    # Example check (database, cache etc.)
    # Right now return ready always
    return {"status": "ready"}