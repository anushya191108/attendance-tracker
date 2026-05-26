from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        attended INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    data = cur.fetchall()
    subjects = []
    for row in data:
        id = row["id"]
        name = row["name"]
        attended = row["attended"]
        total = row["total"]
        percentage = (attended / total * 100) if total > 0 else 0
        can_skip = int((attended / 0.75) - total) if total > 0 else 0
        subjects.append({
            "id": id,
            "name": name,
            "attended": attended,
            "total": total,
            "percentage": round(percentage, 2),
            "can_skip": can_skip,
            "warning": percentage < 75
        })
    conn.close()
    return render_template("index.html", subjects=subjects)
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO data (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/update/<int:id>/<string:action>")
def update(id, action):
    conn = get_db()
    cur = conn.cursor()
    if action == "present":
        cur.execute(
            "UPDATE data SET attended = attended + 1, total = total + 1 WHERE id = ?",
            (id,)
        )
    else:
        cur.execute(
            "UPDATE data SET total = total + 1 WHERE id = ?",
            (id,)
        )
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM data WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)