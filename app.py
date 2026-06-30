import os
import numpy as np
import joblib

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from auth import init_auth, create_user, authenticate_user, User

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)

# IMPORTANT: needed for sessions (DON'T REMOVE)
app.config["SECRET_KEY"] = "CHANGE_THIS_TO_STRONG_SECRET_KEY"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# LOGIN MANAGER (IMPORTANT FIX)
# =========================
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# =========================
# LOAD MODEL
# =========================
model_path = os.path.join(BASE_DIR, "model", "house_model.pkl")
features_path = os.path.join(BASE_DIR, "model", "features.pkl")

model = joblib.load(model_path)
features = joblib.load(features_path)

# =========================
# INIT AUTH SYSTEM
# =========================
init_auth(app)


# =========================
# USER LOADER (IMPORTANT FIX)
# =========================
@login_manager.user_loader
def load_user(user_id):
    from auth import load_users
    users = load_users()

    user_data = users.get(str(user_id))
    if not user_data:
        return None

    return User(
        user_data["id"],
        user_data["username"],
        user_data["password_hash"]
    )


# =========================
# HOME PAGE
# =========================
@app.route("/")
@login_required
def home():
    return render_template(
        "index.html",
        username=current_user.username,
        features=features
    )


# =========================
# PREDICT ROUTE
# =========================
@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        input_values = []

        for feature in features:
            value = request.form.get(feature)

            if value is None or value == "":
                return jsonify({
                    "success": False,
                    "error": f"Missing: {feature}"
                })

            input_values.append(float(value))

        prediction = model.predict([input_values])[0]
        prediction = max(0, prediction)

        return jsonify({
            "success": True,
            "prediction": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# =========================
# LOGIN (FIXED)
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user, error = authenticate_user(username, password)

        if user:
            login_user(user, remember=remember)

            print("LOGIN SUCCESS:", user.username)  # DEBUG

            return redirect(url_for("home"))  # MUST redirect

        print("LOGIN FAILED")  # DEBUG

        return render_template("login.html", error=error)

    return render_template("login.html")


# =========================
# SIGNUP
# =========================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user, error = create_user(username, password)

        if user:
            return redirect(url_for("login"))

        return render_template("signup.html", error=error)

    return render_template("signup.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)