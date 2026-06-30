import json
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

USER_DB_FILE = "users.json"


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = str(id)
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}

    try:
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)


def create_user(username, password):
    users = load_users()

    for u in users.values():
        if u["username"] == username:
            return None, "Username already exists"

    new_id = str(len(users) + 1)

    hashed = generate_password_hash(password)  # IMPORTANT

    users[new_id] = {
        "id": new_id,
        "username": username,
        "password_hash": hashed
    }

    save_users(users)

    return User(new_id, username, hashed), None


def authenticate_user(username, password):
    users = load_users()

    for u in users.values():
        if u["username"] == username:

            user = User(u["id"], u["username"], u["password_hash"])

            if user.check_password(password):
                return user, None

            return None, "Wrong password"

    return None, "User not found"


def init_auth(app):
    pass