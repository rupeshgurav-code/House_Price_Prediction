from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import json
import os

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"  # Change this in production

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# Get base directory (works for local and Vercel)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == 'api':
    BASE_DIR = os.path.dirname(BASE_DIR)

# Load model and scaler
model = joblib.load(os.path.join(BASE_DIR, "model", "house_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "model", "scaler.pkl"))

# User database file
USER_DB_FILE = os.path.join(BASE_DIR, "users.json")


# ============== User Model ==============
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ============== User Database Functions ==============
def load_users():
    """Load users from JSON file."""
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    """Save users to JSON file."""
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)


def create_user(username, password):
    """Create a new user."""
    users = load_users()
    
    # Check if username already exists
    for user_id, user_data in users.items():
        if user_data["username"] == username:
            return None, "Username already exists"
    
    # Generate new user ID
    new_id = str(max([int(uid) for uid in users.keys()], default=0) + 1)
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Create user
    users[new_id] = {
        "id": new_id,
        "username": username,
        "password_hash": password_hash
    }
    
    save_users(users)
    return User(new_id, username, password_hash), None


def authenticate_user(username, password):
    """Authenticate a user."""
    users = load_users()
    
    for user_data in users.values():
        if user_data["username"] == username:
            user = User(user_data["id"], user_data["username"], user_data["password_hash"])
            if user.check_password(password):
                return user, None
            return None, "Invalid password"
    
    return None, "User not found"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    users = load_users()
    user_data = users.get(str(user_id))
    if user_data:
        return User(user_data["id"], user_data["username"], user_data["password_hash"])
    return None


# ============== Auth Routes ==============
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user, error = authenticate_user(username, password)
        
        if user:
            login_user(user)
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        else:
            flash(error, "danger")
    
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # Validate passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template("signup.html")
        
        # Validate password length
        if len(password) < 4:
            flash("Password must be at least 4 characters long.", "danger")
            return render_template("signup.html")
        
        # Create user
        user, error = create_user(username, password)
        
        if user:
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))
        else:
            flash(error, "danger")
    
    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ============== Main Routes ==============
@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html", username=current_user.username)
    return redirect(url_for("login"))


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        # Get form inputs
        area = float(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bathrooms = int(request.form["bathrooms"])
        floor = int(request.form["floor"])
        total_floors = int(request.form["total_floors"])
        furnished = int(request.form["furnished"])
        balcony = int(request.form["balcony"])
        age_of_house = int(request.form["age_of_house"])
        parking = int(request.form["parking"])
        near_school = int(request.form["near_school"])
        near_metro = int(request.form["near_metro"])

        # Create feature array (order must match training data)
        features = np.array([[area, bedrooms, bathrooms, floor, total_floors,
                              furnished, balcony, age_of_house, parking,
                              near_school, near_metro]])

        # Apply scaler
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)[0]

        # Avoid negative values
        prediction = max(0, prediction)
        print(model.score)

        return render_template(
            "index.html",
            prediction_text=f"Estimated House Price: ₹ {prediction:,.2f}",
            username=current_user.username
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            username=current_user.username
        )


if __name__ == "__main__":
    app.run(debug=True)
