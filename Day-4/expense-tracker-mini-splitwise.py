import json
import os
import matplotlib.pyplot as plt

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "groups": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def signup():
    username = input("Create username: ")
    if username in data["users"]:
        print("User already exists")
        return None
    password = input("Create password: ")
    data["users"][username] = password
    save_data(data)
    print("Signup successful")
    return username

def login():
    username = input("Username: ")
    password = input("Password: ")
    if data["users"].get(username) == password:
        print("Login successful")
        return username
    print("Invalid credentials")
    return None

def create_group(user):
    group = input("Group name: ")
    members = input("Members (comma separated): ").split(",")
    members = list(set([m.strip() for m in members] + [user]))

    data["groups"][group] = {
        "members": members,
        "expenses": [],
        "balances": {m: {} for m in members}
    }
    save_data(data)
    print("Group created")

def add_expense(user):
    group = input("Group name: ")
    if group not in data["groups"]:
        print("Group not found")
        return

    amount = float(input("Amount: "))
    category = input("Category (Food/Travel/Shopping/Other): ")
    payer = user

    members = data["groups"][group]["members"]
    split = amount / len(members)

    if amount > 500:
        print("High expense detected")

    for m in members:
        if m != payer:
            data["groups"][group]["balances"][m][payer] = \
                data["groups"][group]["balances"][m].get(payer, 0) + split
            data["groups"][group]["balances"][payer][m] = \
                data["groups"][group]["balances"][payer].get(m, 0) - split

    data["groups"][group]["expenses"].append({
        "payer": payer,
        "amount": amount,
        "category": category
    })

    save_data(data)
    print("Expense added")

def show_balances(user):
    group = input("Group name: ")
    if group not in data["groups"]:
        print("Group not found")
        return

    print("\n--- Balances ---")
    for person, amt in data["groups"][group]["balances"][user].items():
        if amt > 0:
            print(person, "owes you ₹", round(amt, 2))
        elif amt < 0:
            print("You owe", person, "₹", round(-amt, 2))
    print("----------------")

def expense_graph(user):
    group = input("Group name: ")
    if group not in data["groups"]:
        print("Group not found")
        return

    categories = {}
    for e in data["groups"][group]["expenses"]:
        if e["payer"] == user:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

    if not categories:
        print("No expenses to show")
        return

    plt.bar(categories.keys(), categories.values())
    plt.title(f"{user}'s Spending Breakdown")
    plt.ylabel("Amount")
    plt.show()

def dashboard(user):
    while True:
        print("""
======== MENU ========
1. Create Group
2. Add Expense
3. View Balances
4. Expense Graph
5. Logout
======================
""")
        choice = input("Choose: ")

        if choice == "1":
            create_group(user)
        elif choice == "2":
            add_expense(user)
        elif choice == "3":
            show_balances(user)
        elif choice == "4":
            expense_graph(user)
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def main():
    while True:
        print("""
==== SPLITWISE APP ====
1. Signup
2. Login
3. Exit
======================
""")
        choice = input("Choose: ")

        if choice == "1":
            user = signup()
            if user:
                dashboard(user)
        elif choice == "2":
            user = login()
            if user:
                dashboard(user)
        elif choice == "3":
            break
        else:
            print("Invalid option")

main()