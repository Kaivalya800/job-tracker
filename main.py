import json
import os
import sqlite3
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

DB_FILE = "tracker.db"
OLD_JSON = "apps.json"

app = FastAPI()


class Application(BaseModel):
    company: str
    role: str
    status: str
    date_applied: str = ""
    referral: str = ""
    link: str = ""


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT DEFAULT '',
            referral TEXT DEFAULT '',
            link TEXT DEFAULT ''
        )
    """)
    # one-time import of your old apps.json data
    count = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    if count == 0 and os.path.exists(OLD_JSON):
        with open(OLD_JSON, "r") as f:
            old = json.load(f)
        for a in old:
            conn.execute(
                "INSERT INTO applications (id, company, role, status, date_applied, referral, link) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    a.get("id", str(uuid.uuid4())),
                    a["company"],
                    a["role"],
                    a["status"],
                    a.get("date_applied", ""),
                    a.get("referral", ""),
                    a.get("link", ""),
                ),
            )
    conn.commit()
    conn.close()


init_db()


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/applications")
def get_applications():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM applications").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/applications")
def add_application(application: Application):
    entry = application.model_dump()
    entry["id"] = str(uuid.uuid4())
    conn = get_conn()
    conn.execute(
        "INSERT INTO applications (id, company, role, status, date_applied, referral, link) "
        "VALUES (:id, :company, :role, :status, :date_applied, :referral, :link)",
        entry,
    )
    conn.commit()
    conn.close()
    return entry


@app.put("/applications/{app_id}")
def update_application(app_id: str, application: Application):
    data = application.model_dump()
    data["id"] = app_id
    conn = get_conn()
    cur = conn.execute(
        "UPDATE applications SET company=:company, role=:role, status=:status, "
        "date_applied=:date_applied, referral=:referral, link=:link WHERE id=:id",
        data,
    )
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return data


@app.delete("/applications/{app_id}")
def delete_application(app_id: str):
    conn = get_conn()
    cur = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"deleted": app_id}