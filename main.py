import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uuid
from fastapi import HTTPException



FILENAME = "apps.json"

app = FastAPI()


def load_apps():
    apps = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            apps = json.load(f)
    changed = False
    for a in apps:
        if "id" not in a:
            a["id"] = str(uuid.uuid4())
            changed = True
    if changed:
        save_apps(apps)
    return apps


@app.get("/applications")
def get_applications():
    return load_apps()

class Application(BaseModel):
    company: str
    role: str
    status: str
    date_applied: str = ""
    referral: str = ""
    link: str = ""


def save_apps(apps):
    with open(FILENAME, "w") as f:
        json.dump(apps, f, indent=2)


@app.post("/applications")
def add_application(application: Application):
    apps = load_apps()
    entry = application.model_dump()
    entry["id"] = str(uuid.uuid4())
    apps.append(entry)
    save_apps(apps)
    return entry

@app.get("/")
def home():
    return FileResponse("index.html")

@app.put("/applications/{app_id}")
def update_application(app_id: str, application: Application):
    apps = load_apps()
    for a in apps:
        if a["id"] == app_id:
            a.update(application.model_dump())
            save_apps(apps)
            return a
    raise HTTPException(status_code=404, detail="Application not found")


@app.delete("/applications/{app_id}")
def delete_application(app_id: str):
    apps = load_apps()
    remaining = [a for a in apps if a["id"] != app_id]
    if len(remaining) == len(apps):
        raise HTTPException(status_code=404, detail="Application not found")
    save_apps(remaining)
    return {"deleted": app_id}