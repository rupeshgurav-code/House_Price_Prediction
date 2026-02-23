from flask import Flask
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

# Initialize Flask app for auth (will be configured in app.py)
login_manager = LoginManager()

# User database file
USER_DB_FILE = "users.json"


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


def init_auth(app):
    """Initialize authentication with Flask app."""
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
