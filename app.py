from flask import Flask, request, redirect
import os, sqlite3
from urllib.parse import urlparse

app = Flask(__name__)
DB = os.getenv("DATABASE_URL", "urls.db").split("///")[-1]

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS urls (id TEXT PRIMARY KEY, url TEXT NOT NULL);")
    con.commit()
    con.close()

@app.before_first_request
def setup():
    init_db()

@app.route("/<short_id>")
def redirect_short(short_id):
    con = sqlite3.connect(DB)
    cur = con.execute("SELECT url FROM urls WHERE id=?", (short_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return redirect(row[0])
    return "Not found", 404

@app.route("/_new", methods=["POST"])
def create_short():
    data = request.json
    url = data.get("url")
    if not url or not urlparse(url).scheme:
        return {"error": "Invalid URL"}, 400
    short_id = os.urandom(3).hex()
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO urls (id, url) VALUES (?, ?)", (short_id, url))
    con.commit()
    con.close()
    return {"short_url": f"https://{os.getenv('DOMAIN')}/{short_id}"}