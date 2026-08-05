import json
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "annotations.db"

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            labels_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            external_id TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(project_id, external_id)
        );
        CREATE TABLE IF NOT EXISTS annotations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL UNIQUE,
            label TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            annotator TEXT NOT NULL DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

def create_project(name, description, labels):
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO projects(name,description,labels_json) VALUES(?,?,?)",
            (name, description, json.dumps(labels))
        )
        return cur.lastrowid

def get_project(project_id):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM projects WHERE id=?", (project_id,)
        ).fetchone()
        if not row:
            return None
        result = dict(row)
        result["labels"] = json.loads(result.pop("labels_json"))
        return result

def all_projects():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["labels"] = json.loads(item.pop("labels_json"))
            result.append(item)
        return result

def create_item(project_id, external_id, text):
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO items(project_id,external_id,text) VALUES(?,?,?)",
            (project_id, external_id, text)
        )
        return cur.lastrowid

def get_item(item_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None

def project_items(project_id):
    with connect() as conn:
        rows = conn.execute('''
        SELECT i.id,i.project_id,i.external_id,i.text,i.created_at,
               a.label,a.notes,a.annotator,a.updated_at
        FROM items i
        LEFT JOIN annotations a ON a.item_id=i.id
        WHERE i.project_id=?
        ORDER BY i.id
        ''', (project_id,)).fetchall()
        return [dict(r) for r in rows]

def save_annotation(item_id, label, notes, annotator):
    with connect() as conn:
        conn.execute('''
        INSERT INTO annotations(item_id,label,notes,annotator)
        VALUES(?,?,?,?)
        ON CONFLICT(item_id) DO UPDATE SET
          label=excluded.label,
          notes=excluded.notes,
          annotator=excluded.annotator,
          updated_at=CURRENT_TIMESTAMP
        ''', (item_id, label, notes, annotator))
