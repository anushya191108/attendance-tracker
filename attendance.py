from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anush@b1918",
        database="attendance"
    )
@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    data = cur.fetchall()
    subjects = []
    for row in data:
        id, name, attended, total = row
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
    cur.execute("INSERT INTO data (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/update/<int:id>/<string:action>")
def update(id, action):
    conn = get_db()
    cur = conn.cursor()
    if action == "present":
        cur.execute("UPDATE data SET attended = attended+1, total=total+1 WHERE id=%s", (id,))
    else:
        cur.execute("UPDATE data SET total=total+1 WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)