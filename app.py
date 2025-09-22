from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# ---------- Database helper ----------
def db_connection():
    conn = sqlite3.connect("companies.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Init DB ----------
def init_db():
    conn = db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            lastinv TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Test routes ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API kører! 🎉"})

@app.route("/tokens", methods=["GET"])
def get_tokens():
    return jsonify({"status": "ok"})

# ---------- Ekstra ruter ----------
@app.route("/polipo/bodybody", methods=["GET"])
def polipo_bodybody():
    return jsonify({"message": "Denne side virker nu!"})

@app.route("/api/jobs/today", methods=["GET"])
def jobs_today():
    return jsonify({
        "jobs": [],
        "status": "ok",
        "note": "Ingen jobs fundet i dag"
    })

@app.route("/api/v1/body", methods=["GET"])
def api_body():
    industry = request.args.get("industry") or "ukendt"
    location = request.args.get("location") or "ukendt"
    return jsonify({
        "industry": industry,
        "location": location,
        "x": 0.34,
        "y": 1
    })

@app.route("/identity/api/v1/job/today", methods=["GET"])
def identity_job_today():
    return jsonify({"jobs": [], "status": "ok"})

# ---------- Companies CRUD ----------
@app.route("/companies", methods=["GET"])
def get_companies():
    conn = db_connection()
    companies = [dict(row) for row in conn.execute("SELECT * FROM companies")]
    conn.close()
    return jsonify(companies)

@app.route("/companies/<int:company_id>", methods=["GET"])
def get_company(company_id):
    conn = db_connection()
    row = conn.execute("SELECT * FROM companies WHERE id=?", (company_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Company not found"}), 404

@app.route("/companies", methods=["POST"])
def add_company():
    data = request.get_json() or {}
    name = data.get("name")
    industry = data.get("industry")
    lastinv = data.get("lastinv")

    if not name or not industry or not lastinv:
        return jsonify({"error": "Name, industry og lastinv er påkrævet"}), 400

    conn = db_connection()
    cursor = conn.execute(
        "INSERT INTO companies (name, industry, lastinv) VALUES (?, ?, ?)",
        (name, industry, lastinv)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": f"Company med id {new_id} oprettet"}), 201

@app.route("/companies/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    data = request.get_json() or {}
    name = data.get("name")
    industry = data.get("industry")
    lastinv = data.get("lastinv")

    if not name or not industry or not lastinv:
        return jsonify({"error": "Name, industry og lastinv er påkrævet"}), 400

    conn = db_connection()
    conn.execute(
        "UPDATE companies SET name=?, industry=?, lastinv=? WHERE id=?",
        (name, industry, lastinv, company_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"Company med id {company_id} opdateret"})

@app.route("/companies/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    conn = db_connection()
    conn.execute("DELETE FROM companies WHERE id=?", (company_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Company med id {company_id} slettet"})

# ---------- Search ----------
@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    industry = request.args.get("industry")

    query = "SELECT * FROM companies WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if industry:
        query += " AND industry LIKE ?"
        params.append(f"%{industry}%")

    conn = db_connection()
    results = [dict(row) for row in conn.execute(query, params)]
    conn.close()

    if not results:
        return jsonify({"error": "No companies found"}), 404

    return jsonify(results)

# ---------- Start server ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
