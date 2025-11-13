<div align="center">
  
# 🚗 **ParkSmart: Automated Transparent Parking Billing System**

### _Smart, Fair, and Transparent Parking for a Digital World_

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/Backend-Flask-orange.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen.svg)
![API](https://img.shields.io/badge/API-Plate--Recognizer-blueviolet.svg)
![Payment](https://img.shields.io/badge/Payment-Razorpay-lightblue.svg)

</div>

## 🌟 **Overview**

> **ParkSmart** is an AI-driven, IoT-enabled, and cloud-powered **automated parking billing system** that ensures **honest, transparent, and convenient** billing for all parking users.  

It replaces outdated paper tickets and manual billing with a **camera-based number plate recognition system** integrated with **digital payments**.

### 🎯 **Key Highlights**
- 🧠 Automatic Number Plate Recognition (ANPR)  
- 💳 Online Payment via Razorpay (UPI, Wallets, Cards)  
- 📊 Real-Time Parking Session Tracking  
- 📱 User Dashboard for Vehicle Management  
- 💰 Transparent Time-Based Billing  
- ☁️ Cloud Database using MongoDB  

---

### 🎯 **Deployed At**
https://parksmart-u0yf.onrender.com

---

## 🧩 **System Architecture**

```
    ┌────────────────────────────┐
    │       User Device          │
    │ (Signup / Login / Dashboard)│
    └──────────────┬─────────────┘
                   │  HTTPS (Flask API)
    ┌──────────────▼──────────────┐
    │        Flask Backend        │
    │ Routes: /signup /login /pay │
    │ Logic: Billing + Sessions   │
    └──────────────┬──────────────┘
                   │
     ┌─────────────▼──────────────┐
     │   ANPR (Plate Recognizer)  │
     │ Detects plate via camera   │
     └─────────────┬──────────────┘
                   │
     ┌─────────────▼──────────────┐
     │       MongoDB Atlas        │
     │ Stores users, plates, logs │
     └─────────────┬──────────────┘
                   │
     ┌─────────────▼──────────────┐
     │ Razorpay Payment Gateway   │
     │ Handles secure payments    │
     └────────────────────────────┘
```

---

## ⚙️ **Tech Stack**

| Category | Technology |
|-----------|-------------|
| **Backend** | Flask (Python) |
| **Database** | MongoDB (via Flask-PyMongo) |
| **Machine Vision** | Plate Recognizer API |
| **Frontend** | HTML, CSS, JS (Jinja Templates) |
| **Payment Gateway** | Razorpay |
| **Environment** | Python-dotenv for API Keys |
| **Hosting (optional)** | Render / AWS EC2 / Railway |

---

## 🚀 **Features**

| Feature | Description |
|----------|-------------|
| 🔐 **Signup/Login** | Secure authentication with user data stored in MongoDB |
| 🚘 **License Plate Management** | Register, edit, or delete multiple vehicles |
| 📷 **Automatic Detection** | ANPR system identifies vehicle entry/exit |
| 🕒 **Real-Time Timer** | Tracks parking duration automatically |
| 💵 **Automated Billing** | Calculates charge based on parked duration |
| 📄 **Digital Receipt** | Generates e-bill upon exit |
| 💳 **Online Payment** | Integrated with Razorpay for cashless transactions |
| 📈 **Dashboard View** | Displays live session and billing info |

---

## 🧠 **User Stories**

- As a user, I want to **sign up** and create my account.  
- As a user, I want to **log in** securely to manage my parking details.  
- As a user, I want to **register my vehicle’s license plate** to track sessions automatically.  
- As a user, I want the **system to auto-detect entry and exit** via the camera.  
- As a user, I want to **see my live parking status and bill**.  
- As a user, I want to **pay online and receive a digital receipt**.  

---

## 🧩 **System Workflow**

1. **User Registration:** User signs up using email & password.  
2. **Vehicle Registration:** User adds their vehicle license plate.  
3. **Automatic Detection:** ANPR camera sends the image to backend → plate extracted.  
4. **Session Start:** Timer starts automatically for that plate.  
5. **Session End:** On exit detection, session ends.  
6. **Bill Calculation:** Backend computes bill based on duration.  
7. **Payment Gateway:** Razorpay integration handles digital payments.  
8. **Receipt Generation:** User receives a digital receipt.

---

## 🧪 **Testing**

| Test Category | Description |
|----------------|-------------|
| **Unit Tests** | Tested each Flask route (signup, login, payment) |
| **Integration Tests** | Verified ANPR + Billing + Razorpay flow |
| **User Tests** | Validated registration, billing accuracy, and payment confirmation |
| **Edge Cases** | Invalid plates, duplicate entries, failed payment recovery |

---

## 💡 **Challenges Faced**

| Challenge | Solution |
|------------|-----------|
| Integrating ANPR API | Used Plate Recognizer REST API with secure token auth |
| Accurate Time Tracking | Implemented UNIX timestamp-based duration billing |
| Payment Verification | Added Razorpay signature verification route |
| MongoDB Consistency | Used flags for session state (active/inactive) |
| Error Handling | Flash messages for invalid login & unregistered plates |

---

## 🌍 **Social & Market Impact**

> ParkSmart is not just a tech product — it’s a **social impact solution**.  
It brings **transparency, fairness, and trust** to everyday parking systems.

- Eliminates manual errors and overcharging  
- Promotes **digital, cashless payments**  
- Reduces corruption in public parking  
- Aligns with **Smart City** and **Digital India** initiatives  
- Scalable to malls, airports, hospitals, and metros  

---

## 💸 **Investment Appeal**

| Type | Benefit |
|------|----------|
| **Financial** | Scalable SaaS model for parking operators |
| **Social** | Empowers citizens with transparent billing |
| **Research** | Potential for future AI + IoT integration |

---

## 🧭 **Future Scope**

- 📡 IoT-based Slot Tracking  
- 🧾 Dynamic Pricing System  
- 🔊 Voice Alerts for Entry/Exit  
- 🪙 Integration with Smart City APIs  
- 🌐 Mobile App Companion  

---

## 🧰 **Setup Instructions**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Bedangi/ucs503p-202526odd-404notfound.git
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create a `.env` File

```env
FLASK_SECRET_KEY=your_secret
MONGO_URI=your_mongo_uri
PLATE_RECOGNIZER_API_KEY=your_api_key
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

### 4️⃣ Run the Server

```bash
python app.py
```

Then visit 👉 **[http://localhost:5000](http://localhost:5000)**

---

## 👥 **Team & Roles**

| Role              | Responsibility                            |
| ----------------- | ----------------------------------------- |
| Backend Developer | Flask APIs, MongoDB, Razorpay Integration |
| AI Developer      | ANPR (Plate Recognition)                  |
| UI/UX Designer    | Dashboard and user flow                   |
| Tester            | End-to-end system validation              |

---

## 🏁 **Conclusion**

> **ParkSmart** makes parking smarter, payments easier, and billing transparent.
> By combining **machine vision**, **cloud databases**, and **fintech**, it brings trust back to public systems.

> *“Automation is not about replacing people — it’s about making systems fairer for everyone.”*

---

<div align="center">

⭐ **If you like this project, give it a star on GitHub!**
📬 Feedback and contributions are welcome.

</div>
