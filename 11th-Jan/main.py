import auth
import banking
import sys
import time

def clear_screen():
    print("\n" * 2)

def print_header(title):
    print("\n" + "=" * 40)
    print(f" {title.center(36)} ")
    print("=" * 40)

def main_menu():
    while True:
        print_header("BANKING SYSTEM CLI")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            login_flow()
        elif choice == '2':
            register_flow()
        elif choice == '3':
            print("\nThank you for using our Banking System. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def register_flow():
    print_header("REGISTER USER")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    success, message = auth.register_user(username, password)
    print(f"\n{message}")
    if success:
        time.sleep(1)

def login_flow():
    print_header("LOGIN")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    success, message = auth.login_user(username, password)
    if success:
        print(f"\n{message}")
        user_dashboard(username)
    else:
        print(f"\n{message}")

def user_dashboard(username):
    while True:
        print_header(f"WELCOME, {username.upper()}")
        print("1. Create New Account")
        print("2. My Accounts")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. View Statement")
        print("7. Logout")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            create_account_flow(username)
        elif choice == '2':
            list_accounts(username)
        elif choice == '3':
            transaction_flow(username, 'DEPOSIT')
        elif choice == '4':
            transaction_flow(username, 'WITHDRAW')
        elif choice == '5':
            list_accounts(username) # Simplest way to check balance
        elif choice == '6':
            view_statement_flow(username)
        elif choice == '7':
            print("\nLogging out...")
            break
        else:
            print("Invalid choice.")

def view_statement_flow(username):
    print_header("ACCOUNT STATEMENT")
    accounts = banking.get_user_accounts(username)
    if not accounts:
        print("No accounts found.")
        return

    print("Available Accounts:")
    acc_list = list(accounts.keys())
    for idx, acc in enumerate(acc_list, 1):
        print(f"{idx}. {acc} ({accounts[acc]['type']})")
        
    choice = input("\nSelect Account (Number): ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(acc_list):
            account_num = acc_list[idx]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    transactions = banking.get_account_transactions(account_num)
    if not transactions:
        print("\nNo transactions found for this account.")
    else:
        print(f"\nTransaction History for {account_num}:")
        print(f"{'TIMESTAMP':<25} | {'TYPE':<10} | {'AMOUNT':<10} | {'STATUS'}")
        print("-" * 65)
        for t in transactions:
            print(f"{t['timestamp']:<25} | {t['type']:<10} | {t['amount']:<10} | {t['status']}")
    
    input("\nPress Enter to continue...")

def create_account_flow(username):
    print_header("OPEN NEW ACCOUNT")
    print("Select Account Type:")
    print("1. Savings")
    print("2. Current")
    
    type_choice = input("Choice: ")
    acc_type = "Savings" if type_choice == '1' else "Current" if type_choice == '2' else None
    
    if not acc_type:
        print("Invalid account type selected.")
        return

    account_num = banking.create_account(username, acc_type)
    print(f"\nAccount created successfully!")
    print(f"Account Number: {account_num}")
    print(f"Type: {acc_type}")

def list_accounts(username):
    print_header("MY ACCOUNTS")
    accounts = banking.get_user_accounts(username)
    if not accounts:
        print("No accounts found.")
        return None
    
    for acc_num, data in accounts.items():
        print(f"Account: {acc_num} | Type: {data['type']} | Balance: ₹{data['balance']}")
    
    return accounts

def transaction_flow(username, trans_type):
    print_header(f"{trans_type} FUNDS")
    accounts = banking.get_user_accounts(username)
    if not accounts:
        print("No accounts found. Please create one first.")
        return
    
    # Simple selection if multiple accounts, or just type it in
    print("Available Accounts:")
    acc_list = list(accounts.keys())
    for idx, acc in enumerate(acc_list, 1):
        print(f"{idx}. {acc} ({accounts[acc]['type']} - ₹{accounts[acc]['balance']})")
        
    choice = input("\nSelect Account (Number): ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(acc_list):
            account_num = acc_list[idx]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
        
    try:
        amount = float(input(f"Enter amount to {trans_type.lower()}: "))
    except ValueError:
        print("Invalid amount.")
        return
        
    success, msg = banking.process_transaction(account_num, trans_type, amount)
    print(f"\n{msg}")

if __name__ == "__main__":
    # Ensure data files exist
    import data_manager 
    for filename in data_manager.DEFAULTS:
        data_manager.load_data(filename)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()
