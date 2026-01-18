import json
import os

DEFAULTS = {
    "users.json": [],
    "accounts.json": {},
    "transactions.json": []
}

def load_data(filename):
    if not os.path.exists(filename):
        save_data(filename, DEFAULTS.get(filename, []))
        return DEFAULTS.get(filename, [])
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return DEFAULTS.get(filename, [])

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
