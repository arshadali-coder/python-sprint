# Banking System CLI

A robust command-line based banking application allowing users to manage accounts, perform transactions, and view audit logs.

## 🚀 Features

-   **User Authentication**: Secure Registration and Login with password hashing.
-   **Account Management**: Create Savings and Current accounts with auto-generated account numbers.
-   **Transaction Engine**: 
    -   Deposit and Withdraw funds.
    -   Real-time balance updates.
    -   View transaction history/statements.
-   **Business Rules**:
    -   Prevents negative deposits.
    -   Prevents overdrafts (cannot withdraw more than balance).
    -   Minimum balance checks for Savings accounts (₹1000).
    -   Alerts for large withdrawals (> ₹50,000).
-   **Data Persistence**: All data (users, accounts, transactions) is stored in local JSON files.

## 🛠️ Usage

Run the main application file:

```bash
python main.py
```

## 📂 Project Structure

-   `main.py`: Entry point and CLI interface.
-   `auth.py`: Handles user registration and login logic.
-   `banking.py`: Core logic for accounts and transactions.
-   `data_manager.py`: Utilities for reading/writing JSON data.
