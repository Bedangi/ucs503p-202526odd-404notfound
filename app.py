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

# Signup
@app.route("/")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    token = request.form.get("token", "").strip()  # optional

    db = load_db()
    if any(u["email"] == email for u in db["users"]):
        flash("Email already registered. Please login.", "error")
        return redirect(url_for("login_page"))

    user = {
        "username": username,
        "email": email,
        "password": password,
        "token": token if token else None,
        "start_time": None,
        "active": False,
        "bill": 0,
        "plates": []
    }
    db["users"].append(user)
    save_db(db)

    return redirect(url_for("plates_page", email=email))

# Login
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    db = load_db()
    user = next(
        (
            u for u in db.get("users", [])
            if u.get("email") == email and u.get("password") == password
        ),
        None,
    )

    if not user:
        flash("Invalid email or password. Please try again or sign up.", "error")
        return redirect(url_for("login_page"))

    return redirect(url_for("plates_page", email=email))


# Plates Page
@app.route("/plates/<email>")
def plates_page(email):
    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user:
        return "User not found", 404
    return render_template("plates.html", user=user)

@app.route("/plates/<email>", methods=["POST"])
def add_plate(email):
    plate_number = request.form.get("plateNumber")

    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user:
        return "User not found", 404

    if not user.get("plates"):
        user["plates"] = []

    if plate_number not in user["plates"]:
        user["plates"].append(plate_number)
        save_db(db)

    return redirect(url_for("plates_page", email=email))

@app.route("/delete_plate", methods=["POST"])
def delete_plate():
    db = load_db()
    email = request.form.get("email")
    plate = request.form.get("plate")
    user = next((u for u in db["users"] if u["email"] == email), None)
    if user and plate in user["plates"]:
        user["plates"].remove(plate)
        save_db(db)
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/edit_plate", methods=["POST"])
def edit_plate():
    db = load_db()
    email = request.form.get("email")
    old_plate = request.form.get("old_plate")
    new_plate = request.form.get("new_plate")
    user = next((u for u in db["users"] if u["email"] == email), None)
    if user and old_plate in user["plates"]:
        index = user["plates"].index(old_plate)
        user["plates"][index] = new_plate
        save_db(db)
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/dashboard/<email>")
def dashboard(email):
    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user:
        return "User not found", 404
    return render_template("dashboard.html", user=user)

# Parking APIs
@app.route("/scan/<email>", methods=["POST"])
def scan_car(email):
    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["start_time"] = time.time()
    user["active"] = True
    save_db(db)
    return jsonify({"message": "Parking started", "start_time": user["start_time"]})

@app.route("/leave/<email>", methods=["POST"])
def leave_now(email):
    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user or not user["active"]:
        return jsonify({"error": "Car not parked"}), 404

    def delayed_check():
        time.sleep(1)  # 5 sec check
        db2 = load_db()
        u = next((x for x in db2["users"] if x["email"] == email), None)
        if u and u["active"]:
            end_time = time.time()
            duration = (end_time - u["start_time"]) / 3600
            cost = round(duration * 20, 2)
            u["active"] = False
            u["bill"] = cost
            save_db(db2)

    threading.Thread(target=delayed_check).start()
    return jsonify({"message": "Leave request initiated, checking in 5 sec"})

@app.route("/status/<email>")
def status(email):
    db = load_db()
    user = next((u for u in db["users"] if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    response = {"active": user["active"], "bill": user["bill"], "plates": user.get("plates", [])}
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

        db = load_db()
        user = next((u for u in db["users"] if plate in u["plates"]), None)
        requests.post(f"http://localhost:5000/scan/{user["email"]}")

        return f"Detected Plate: {plate}"
    else:
        return "No plate detected"

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
