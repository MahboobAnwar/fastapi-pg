from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os

app = FastAPI()

# ── DB CONNECTION ──────────────────────────────────────────
def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(database_url)

# ── MODEL ──────────────────────────────────────────────────
class User(BaseModel):
    name: str
    email: str | None = None
    age: int | None = None

# ── INSERT ─────────────────────────────────────────────────
@app.post("/users")
def insert_user(user: User):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (user.name, user.email, user.age)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": f"✅ User '{user.name}' inserted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── FETCH ──────────────────────────────────────────────────
@app.get("/users")
def fetch_users():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── DELETE ─────────────────────────────────────────────────
@app.delete("/users/{name}")
def delete_user(name: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE name = %s", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": f"🗑️ User '{name}' deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
