import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse



FILENAME = "apps.json"

app = FastAPI()


def load_apps():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []


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
    apps.append(application.model_dump())
    save_apps(apps)
    return application

@app.get("/")
def home():
    return FileResponse("index.html")