import os
import json
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI(title="Cyber Attack Reporter API")

REPORTS_DIR = "reports"

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Mount the 'web' directory to serve static files (HTML, CSS, JS)
app.mount("/app", StaticFiles(directory="web", html=True), name="web")

@app.get("/api/reports")
def list_reports():
    """List all available report dates."""
    reports = []
    if os.path.exists(REPORTS_DIR):
        for filename in os.listdir(REPORTS_DIR):
            if filename.endswith(".json"):
                # Extract date from YYYY-MM-DD.json
                date_str = filename.replace(".json", "")
                reports.append(date_str)
    
    # Sort dates descending (newest first)
    reports.sort(reverse=True)
    return {"reports": reports}

@app.get("/api/reports/{date_str}")
def get_report(date_str: str):
    """Get the specific JSON report for a date."""
    filepath = os.path.join(REPORTS_DIR, f"{date_str}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    else:
        return JSONResponse(status_code=404, content={"error": "Report not found"})

if __name__ == "__main__":
    import uvicorn
    # Make sure we run from the project root
    print("Starting Web Server on http://localhost:8000/app")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
