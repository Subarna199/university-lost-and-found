from flask import Flask, render_template, request, redirect, url_for, flash
import os, json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if __file__.endswith("app.py") else os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
FILE = os.path.join(DATA_DIR, "lost_found.json")

app = Flask(__name__)
app.secret_key = "dev-secret-shrestha"  # for flash messages; replace in production

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {"lost": [], "found": []}
    return {"lost": [], "found": []}

def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    data = load_data()
    recent_lost = list(reversed(data["lost"]))[:5]
    recent_found = list(reversed(data["found"]))[:5]
    return render_template("index.html", recent_lost=recent_lost, recent_found=recent_found)

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        kind = request.form.get("kind")
        item = request.form.get("item", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()
        description = request.form.get("description", "").strip()
        if not item or not location:
            flash("Please provide at least an item name and location.", "error")
            return redirect(url_for("report"))
        entry = {
            "id": int(datetime.utcnow().timestamp() * 1000),
            "item": item,
            "location": location,
            "contact": contact,
            "description": description,
            "date": datetime.utcnow().isoformat(),
            "status": "Unclaimed" if kind == "found" else "Unreturned"
        }
        data = load_data()
        if kind == "found":
            data["found"].append(entry)
        else:
            data["lost"].append(entry)
        save_data(data)
        flash(f"{'Found' if kind=='found' else 'Lost'} item reported successfully.", "success")
        return redirect(url_for("index"))
    return render_template("report.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    results = {"lost": [], "found": []}
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        data = load_data()
        for entry in data["lost"]:
            if query in entry["item"].lower() or query in entry.get("description", "").lower() or query in entry.get("location", "").lower():
                results["lost"].append(entry)
        for entry in data["found"]:
            if query in entry["item"].lower() or query in entry.get("description", "").lower() or query in entry.get("location", "").lower():
                results["found"].append(entry)
    return render_template("search.html", results=results, query=query)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()
    if request.method == "POST":
        id_str = request.form.get("id")
        kind = request.form.get("kind")
        action = request.form.get("action")
        if id_str and kind and action:
            id_val = int(id_str)
            target_list = data["found"] if kind == "found" else data["lost"]
            for entry in target_list:
                if entry["id"] == id_val:
                    if action == "mark_returned":
                        entry["status"] = "Returned"
                        flash("Item marked as Returned.", "success")
                    elif action == "delete":
                        target_list.remove(entry)
                        flash("Item deleted.", "success")
                    break
            save_data(data)
        return redirect(url_for("admin"))
    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
