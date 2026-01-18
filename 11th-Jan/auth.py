import hashlib
from data_manager import load_data, save_data

USERS_FILE = 'users.json'

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_data(USERS_FILE)
    
    for user in users:
        if user['username'] == username:
            return False, "Username already exists."
    
    new_user = {
        'username': username,
        'password': _hash_password(password)
    }
    users.append(new_user)
    save_data(USERS_FILE, users)
    return True, "User registered successfully."

def login_user(username, password):
    users = load_data(USERS_FILE)
    hashed_pw = _hash_password(password)
    
    for user in users:
        if user['username'] == username and user['password'] == hashed_pw:
            return True, "Login successful."
    
    return False, "Invalid username or password."
