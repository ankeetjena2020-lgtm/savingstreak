import bcrypt
import database as db


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def signup_user(username, password):
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"

    existing = db.get_user_by_username(username)
    if existing:
        return False, "Username already taken"

    password_hash = hash_password(password)
    success = db.create_user(username, password_hash)

    if success:
        return True, "Account created successfully! Please log in."
    else:
        return False, "Something went wrong. Try a different username."


def login_user(username, password):
    user = db.get_user_by_username(username)

    if not user:
        return False, "Username not found"

    if verify_password(password, user["password_hash"]):
        return True, user["user_id"]
    else:
        return False, "Incorrect password"