import json
import time
from pathlib import Path
import sys

def type_print(msg, speed=0.03):
    for ch in msg:
        print(ch, end='', flush=True)
        time.sleep(speed)

greet = "\n📀 Welcome to Vault OS 1.0 — Your Personal Password Commander\n-------------------------------------------------------------\nChoose an operation:\n1. Access stored credentials\n2. Store a new credential\n3. Update existing credential\n4. Remove a saved credential\n5. Shut down Vault OS\n\n"

database = Path(__file__).parent / "database.json"

def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    global data
    try:
        with open(database, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = {}

def main_menu():
    while True:
        clear()
        type_print(greet, 0.01)
        load_data()
        choice = input("--> Vault OS command: ")

        if choice == "1":
            clear()
            show_passwords()
        elif choice == "2":
            clear()
            add_password()
        elif choice == "3":
            clear()
            edit_password()
        elif choice == "4":
            clear()
            del_password()
        elif choice == "5":
            clear()
            type_print("\n🛡️ Shutting down Vault OS... Stay secure, Commander!\n")
            sys.exit()
        else:
            type_print("❌ Invalid command. Please try again.\n")

def show_passwords():
    if not data:
        type_print("⚠️ Vault OS database is empty, Commander.\n")
        return
    else:
        type_print("🔐 Decrypted credentials:\n")
        for key, value in data.items():
            website, username = key.split("_")
            type_print(f"🔸 {username}'s {website} -> {value}\n\n")
        type_print("↩️ Returning to Vault OS menu...\n")

def add_password():
    a = input("🌐 Website: ")
    b = input("👤 Username: ")
    c = input("🔑 Password: ")
    data[f"{a}_{b}"] = c
    with open(database, "w") as f:
        json.dump(data, f, indent=4)
    type_print("💾 Saving to Vault...\n")
    type_print("✅ Operation completed. Returning to menu...\n")

def edit_password():
    if not data:
        type_print("⚠️ Vault OS database is empty.\n")
        return
    else:
        temp_data = {}
        for i, (key, value) in enumerate(data.items(), start=1):
            temp_data[f"key_{i}"] = key
            a, b = key.split("_")
            type_print(f"{i}. {b}'s {a} account -> {value}\n")
        number = input("🛠️ Enter number to update: ")
        while True:
            fstring = f"key_{number}"
            key_in_process = temp_data.get(fstring)
            if key_in_process:
                a1, b1 = key_in_process.split("_")
                new_pass = input(f"🔄 New password for {b1}'s {a1} account: ")
                data[key_in_process] = new_pass
                with open(database, "w") as f:
                    json.dump(data, f, indent=4)
                type_print("✅ Credential updated successfully.\n")
                return
            else:
                type_print("❌ Invalid input. Please retry.\n")
                number = input("--> ")

def del_password():
    if not data:
        type_print("⚠️ Vault OS database is empty.\n")
        return
    else:
        temp_data = {}
        for i, (key, value) in enumerate(data.items(), start=1):
            temp_data[f"key_{i}"] = key
            a, b = key.split("_")
            type_print(f"{i}. {b}'s {a} account -> {value}\n")
        number = input("🧨 Enter number to delete: ")
        while True:
            fstring = f"key_{number}"
            key_in_process = temp_data.get(fstring)
            if key_in_process:
                data.pop(key_in_process)
                with open(database, "w") as f:
                    json.dump(data, f, indent=4)
                type_print("🗑️ Entry deleted. Returning to menu...\n")
                return
            else:
                type_print("❌ Invalid input. Please retry.\n")
                number = input("--> ")

if __name__ == "__main__":
    main_menu()