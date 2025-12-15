from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.environ["DATABASE_URL"]

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.post("/query")
def query(req: dict):
    sql = req.get("sql")

    if not sql:
        return {"error": "No SQL provided"}

    if not sql.lower().startswith("select"):
        return {"error": "Only SELECT allowed"}

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {"result": rows}
