from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import json
import glob

app = FastAPI()

# Allow frontend JS to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/app", StaticFiles(directory="web", html=True), name="web")


@app.get("/api/latest")
def get_latest():
    latest_path = os.path.join("reports", "latest.json")

    if not os.path.exists(latest_path):
        return JSONResponse(status_code=404, content={"detail": "Latest report not found"})

    with open(latest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@app.get("/api/reports")
def list_reports():
    files = sorted(glob.glob(os.path.join("reports", "*.json")), reverse=True)

    dates = []
    for fpath in files:
        name = os.path.basename(fpath)
        if name.lower() == "latest.json":
            continue
        if name.endswith(".json") and len(name) == len("YYYY-MM-DD.json"):
            dates.append(name.replace(".json", ""))

    return {"reports": dates}


@app.get("/api/reports/{date_str}")
def get_report(date_str: str):
    path = os.path.join("reports", f"{date_str}.json")

    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"detail": f"{date_str}.json not found"})

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

    app.mount("/", StaticFiles(directory="web", html=True), name="root")

    from fastapi.responses import FileResponse

@app.get("/favicon.ico")
def favicon():
    path = os.path.join("web", "favicon.ico")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse(status_code=404, content={"detail": "Not found"})

    <<<<<<<
=======
>>>>>>>