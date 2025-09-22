from flask import Flask, request

app = Flask(__name__)

# ---------- Forside & test ----------
@app.route("/")
def home():
    return "Flask kører! 🎉"

@app.route("/ping")
def ping():
    return {"status": "ok"}

# ---------- Jobs ----------
@app.route("/api/jobs/today")
def jobs_today():
    jobs = [
        {"id": 1, "kunde": "Testkunde", "fra": "København", "til": 
"Aarhus", "status": "ikke startet"},
        {"id": 2, "kunde": "Anden kunde", "fra": "Odense", "til": 
"Aalborg", "status": "i gang"}
    ]
    return {"jobs": jobs}

@app.route("/api/jobs/<int:job_id>/start", methods=["POST"])
def start_job(job_id):
    return {"message": f"Job {job_id} startet"}

@app.route("/api/jobs/<int:job_id>/stop", methods=["POST"])
def stop_job(job_id):
    return {"message": f"Job {job_id} stoppet"}

# ---------- Rapporter ----------
@app.route("/api/jobs/<int:job_id>/report", methods=["POST"])
def report_job(job_id):
    data = request.json
    return {"message": f"Rapport modtaget for job {job_id}", "data": data}

# ---------- Upload billeder ----------
@app.route("/api/jobs/<int:job_id>/media", methods=["POST"])
def upload_media(job_id):
    # Her ville vi normalt gemme filen
    return {"message": f"Billede modtaget for job {job_id}"}

# ---------- Start server ----------
if __name__ == "__main__":
    app.run(debug=True)

