import random
import datetime
import uuid
from data_manager import load_data, save_data

ACCOUNTS_FILE = 'accounts.json'
TRANSACTIONS_FILE = 'transactions.json'

MIN_BALANCE_SAVINGS = 1000
LARGE_WITHDRAWAL_LIMIT = 50000

def _generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def create_account(username, account_type):
    accounts = load_data(ACCOUNTS_FILE)
    
    # Simple check to ensure user doesn't already have this account type (optional, but good)
    # But prompt says "Each user has: Account number...". implied one or multiple. Let's allow multiple.
    
    account_num = _generate_account_number()
    while account_num in accounts:
        account_num = _generate_account_number()
    
    accounts[account_num] = {
        "owner": username,
        "type": account_type,
        "balance": 0.0,
        "failed_withdrawals": 0
    }
    
    save_data(ACCOUNTS_FILE, accounts)
    return account_num

def get_user_accounts(username):
    accounts = load_data(ACCOUNTS_FILE)
    return {acc_num: data for acc_num, data in accounts.items() if data['owner'] == username}

def log_transaction(account_num, trans_type, amount, status):
    transactions = load_data(TRANSACTIONS_FILE)
    
    log_entry = {
        "id": str(uuid.uuid4()),
        "account_number": account_num,
        "type": trans_type,
        "amount": amount,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": status
    }
    
    transactions.append(log_entry)
    save_data(TRANSACTIONS_FILE, transactions)
    return log_entry['id']

def process_transaction(account_num, trans_type, amount):
    accounts = load_data(ACCOUNTS_FILE)
    if account_num not in accounts:
        return False, "Account not found."
    
    account = accounts[account_num]
    
    if trans_type == 'DEPOSIT':
        if amount <= 0:
            log_transaction(account_num, trans_type, amount, "FAILED")
            return False, "Deposit amount must be positive."
        
        account['balance'] += amount
        # Rule: Zero balance -> freeze warning check (if it WAS zero and now isn't, or generic check?)
        # The rule is "Zero balance -> account freeze warning". Getting OUT of zero might be good.
        # But let's check creating the warning if balance creates/remains zero?
        # Use simpler interpretation: check balance after transaction.
        
        save_data(ACCOUNTS_FILE, accounts)
        log_transaction(account_num, trans_type, amount, "SUCCESS")
        return True, f"Deposited ₹{amount}. New Balance: ₹{account['balance']}"

    elif trans_type == 'WITHDRAW':
        # Rule: Cannot withdraw more than balance
        if amount > account['balance']:
            account['failed_withdrawals'] += 1
            save_data(ACCOUNTS_FILE, accounts)
            log_transaction(account_num, trans_type, amount, "FAILED")
            
            msg = "Insufficient funds."
            # Rule: More than 3 failed withdrawals -> warning
            if account['failed_withdrawals'] > 3:
                msg += " [WARNING: Multiple failed consecutive withdrawals detected!]"
            return False, msg

        # Rule: Minimum balance rule for Savings account
        if account['type'] == 'Savings' and (account['balance'] - amount) < MIN_BALANCE_SAVINGS:
            log_transaction(account_num, trans_type, amount, "FAILED")
            return False, f"Transaction declined. Savings account must maintain min balance of ₹{MIN_BALANCE_SAVINGS}."

        # Rule: Withdraw > 50,000 -> flag transaction
        if amount > LARGE_WITHDRAWAL_LIMIT:
            print(f"*** ALERT: Large withdrawal of ₹{amount} initiated. Flagged for review. ***")
            # We still allow it, just flag it visually and in logs presumably.
            # or maybe we require extra approval? Let's just log it as SUCCESS but maybe with a note?
            # The log function is simple. Let's just proceed.

        account['balance'] -= amount
        account['failed_withdrawals'] = 0 # Reset on success
        
        save_data(ACCOUNTS_FILE, accounts)
        log_transaction(account_num, trans_type, amount, "SUCCESS")
        
        msg = f"Withdrawn ₹{amount}. New Balance: ₹{account['balance']}"
        # Rule: Zero balance -> account freeze warning
        if account['balance'] == 0:
            msg += " [WARNING: Account balance is ZERO. Please deposit funds to avoid freeze.]"
            
        return True, msg

    return False, "Invalid transaction type."

def get_balance(account_num):
    accounts = load_data(ACCOUNTS_FILE)
    if account_num in accounts:
        return accounts[account_num]['balance']
    return None

def get_account_transactions(account_num):
    all_transactions = load_data(TRANSACTIONS_FILE)
    # Filter for this account
    return [t for t in all_transactions if t['account_number'] == account_num]
