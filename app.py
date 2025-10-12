from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_cors import CORS
import requests
import time, threading, razorpay
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://bedasaha789_db_user:5eZT4qYaghR57LoG@cluster0.fyqmenz.mongodb.net/parksmart_db?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
users = mongo.db.users

API_KEY = "500a3d6beb83762f839fae49fff74725ea44fb26" # Scanner API
# Razorpay Test Mode Setup
razorpay_client = razorpay.Client(auth=("rzp_test_RRlePW8ry9sAIu", "T7pMD5f8K9ffHIw1lIOONiX0"))

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

    if users.find_one({"email": email}):
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
        "plates": [],
        "active_plate": None,
        "payment_status": "unpaid"
    }
    users.insert_one(user)
    return redirect(url_for("plates_page", email=email))

# Login
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = users.find_one({"email": email, "password": password})

    if not user:
        flash("Invalid email or password. Please try again or sign up.", "error")
        return redirect(url_for("login_page"))

    return redirect(url_for("plates_page", email=email))


# Plates Page
@app.route("/plates/<email>")
def plates_page(email):
    user = users.find_one({"email": email})
    if not user:
        return "User not found", 404
    return render_template("plates.html", user=user)

@app.route("/plates/<email>", methods=["POST"])
def add_plate(email):
    plate_number = request.form.get("plateNumber")

    user = users.find_one({"email": email})
    if not user:
        return "User not found", 404

    plates = user.get("plates", [])
    if plate_number not in plates:
        plates.append(plate_number)
        users.update_one({"email": email}, {"$set": {"plates": plates}})

    return redirect(url_for("plates_page", email=email))

@app.route("/delete_plate", methods=["POST"])
def delete_plate():
    email = request.form.get("email")
    plate = request.form.get("plate")
    
    user = users.find_one({"email": email})
    if user and plate in user.get("plates", []):
        plates = user["plates"]
        plates.remove(plate)
        users.update_one({"email": email}, {"$set": {"plates": plates}})
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/edit_plate", methods=["POST"])
def edit_plate():
    email = request.form.get("email")
    old_plate = request.form.get("old_plate")
    new_plate = request.form.get("new_plate")

    user = users.find_one({"email": email})
    if user and old_plate in user.get("plates", []):
        plates = user["plates"]
        index = plates.index(old_plate)
        plates[index] = new_plate
        users.update_one({"email": email}, {"$set": {"plates": plates}})
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/dashboard/<email>")
def dashboard(email):
    user = users.find_one({"email": email})
    if not user:
        return "User not found", 404
    return render_template("dashboard.html", user=user)

@app.route("/leave/<email>", methods=["POST"])
def leave_now(email):
    user = users.find_one({"email": email})
    if not user or not user.get("active"):
        return jsonify({"error": "Car not parked"}), 404

    end_time = time.time()
    duration = (end_time - user["start_time"]) / 3600
    cost = round(duration * 100, 2)
    users.update_one(
        {"email": email},
        {"$set": {"active": False, "bill": cost}}
    )

    return jsonify({"message": "Leave request initiated, checking in 5 sec"})

@app.route("/status/<email>")
def status(email):
    user = users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    response = {
        "active": user.get("active", False),
        "bill": user.get("bill", 0),
        "plates": user.get("plates", []),
        "active_plate": user.get("active_plate")
    }
    if user.get("active"):
        response["start_time"] = user["start_time"]
        response["elapsed"] = round((time.time() - user["start_time"]) / 60, 2)
    return jsonify(response)

# PAYMENT 
@app.route("/pay/<email>")
def pay_now(email):
    user = users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user["bill"] <= 0:
        return jsonify({"error": "No pending bill"}), 400

    try:
        amount = int(user["bill"] * 100)
        if amount < 100:  # Razorpay minimum is 100 paise (1 INR)
            return jsonify({"error": "Amount too small. Minimum is 1 INR"}), 400
            
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": f"receipt_{email}_{int(time.time())}" 
        })
        
        print(f"Order created successfully: {order}")
        return jsonify(order)
        
    except Exception as e:
        print(f"Razorpay order creation failed: {str(e)}")  # This will show the actual error
        return jsonify({"error": f"Failed to create order: {str(e)}"}), 500

@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    data = request.get_json()
    print("Payment received:", data)
    email = data.get("email")
    # Update bill status
    razorpay_client.utility.verify_payment_signature({
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    })
    user = users.find_one({"email": email, "payment_status": "unpaid"})
    if user:
        users.update_one({"_id": user["_id"]}, {"$set": {"bill": 0, "payment_status": "paid"}})
        return jsonify({"success": True, "message": "Payment verified and updated."})

    return jsonify({"success": False, "message": "User not found or already paid."})

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
        user = users.find_one({"plates": plate})
        
        if user:
            users.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "active_plate": plate,
                    "start_time": time.time(),
                    "active": True
                }}
            )
            return f"Detected Plate: {plate}"
        else:
            return f"Detected Plate: {plate}, Plate not registered"
    else:
        return "No plate detected"

@app.route("/bill/<email>")
def bill_page(email):
    user = users.find_one({"email": email})
    if not user:
        return "User not found", 404

    if not user.get("start_time") or not user.get("bill"):
        return "No parking session found for this user", 400

    start_time = user["start_time"]
    end_time = user.get("end_time", time.time())
    duration_seconds = end_time - start_time
    duration_str = str(timedelta(seconds=int(duration_seconds)))
    total_bill = user.get("bill", 0)

    return render_template(
        "bill.html",
        user=user,
        duration=duration_str,
        total_bill=total_bill,
        startTime=format_time(start_time),
        endTime=format_time(end_time)
    )

def format_time(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M:%S")

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
