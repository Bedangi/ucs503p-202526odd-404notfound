from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
import requests
import json, time, threading, os

pytesseract.pytesseract.tesseract_cmd = r"D:\softwares\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"
API_KEY = "500a3d6beb83762f839fae49fff74725ea44fb26"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": []}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    plate = request.form["plate"]

    db = load_db() 
    # Prevent duplicate car plate
    if any(u["plate"] == plate for u in db["users"]):
        flash("Car plate already registered. Please login.", "error")
        return redirect(url_for("login_page"))

    user = {"name": name, "plate": plate, "start_time": None, "active": False, "bill": 0}
    db["users"].append(user)
    save_db(db)

    return redirect(url_for("dashboard", plate=plate))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    plate = request.form.get("plate")

    db = load_db()
    user = next(
        (
            u for u in db.get("users", [])
            if u.get("name") == name and u.get("plate") == plate
        ),
        None,
    )

    if not user:
        flash("Invalid name or car plate. Please try again or sign up.", "error")
        return redirect(url_for("login_page"))

    return redirect(url_for("dashboard", plate=plate))
    
    
@app.route("/dashboard/<plate>")
def dashboard(plate):
    db = load_db()
    user = next((u for u in db["users"] if u["plate"] == plate), None)
    if not user:
        return "User not found", 404
    return render_template("dashboard.html", user=user)

@app.route("/scan/<plate>", methods=["POST"])
def scan_car(plate):
    db = load_db()
    user = next((u for u in db["users"] if u["plate"] == plate), None)
    if not user:
        return jsonify({"error": "Car not found"}), 404

    user["start_time"] = time.time()
    user["active"] = True
    save_db(db)
    return jsonify({"message": "Parking started", "start_time": user["start_time"]})

@app.route("/leave/<plate>", methods=["POST"])
def leave_now(plate):
    db = load_db()
    user = next((u for u in db["users"] if u["plate"] == plate), None)
    if not user or not user["active"]:
        return jsonify({"error": "Car not parked"}), 404

    def delayed_check():
        time.sleep(1)
        db2 = load_db()
        u = next((x for x in db2["users"] if x["plate"] == plate), None)
        if u and u["active"]:
            end_time = time.time()
            duration = (end_time - u["start_time"]) / 3600
            cost = round(duration * 20, 2)
            u["active"] = False
            u["bill"] = cost
            save_db(db2)

    threading.Thread(target=delayed_check).start()
    return jsonify({"message": "Leave request initiated, checking in 30 sec"})

@app.route("/status/<plate>")
def status(plate):
    db = load_db()
    user = next((u for u in db["users"] if u["plate"] == plate), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    response = {"active": user["active"], "bill": user["bill"]}
    if user["active"]:
        response["start_time"] = user["start_time"]
        response["elapsed"] = round((time.time() - user["start_time"]) / 60, 2)
    return jsonify(response)

@app.route('/anpr', methods=['POST'])
def anpr():
    file = request.files['frame']
    files = {"upload": (file.filename, file.stream, file.mimetype)}
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/', files = files, headers={'Authorization': f"Token {API_KEY}"})
    data = response.json()
    print("API Response:", data)

    if data.get("results") and len(data["results"]) > 0:
        plate = data["results"][0]["plate"].upper()
        print("Detected Plate:", plate)

        requests.post(f"http://localhost:5000/scan/{plate}")

        return f"Detected Plate: {plate}"
    else:
        return "No plate detected"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    


