from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

app = FastAPI()
DATABASE_URL ="postgresql://neondb_owner:npg_KNmXR3ryTc8V@ep-square-glade-a13ch26i-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# ── DB CONNECTION ──────────────────────────────────────────
def get_connection():
    return psycopg2.connect(DATABASE_URL)

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