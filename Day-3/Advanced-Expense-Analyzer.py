expenses = []
category_totals = {}
high_expense_count = 0

n = int(input("Enter number of expenses: "))

for i in range(1, n + 1):
    while True:
        amount_input = input(f"\nEnter expense {i} amount: ")
        if amount_input.isdigit():
            amount = int(amount_input)
            break
        else:
            print("Please enter a valid number.")

    category = input("Enter category (Food/Travel/Shopping/Other): ").title()

    expenses.append(amount)

    if amount > 500:
        print("High expense detected")
        high_expense_count += 1

    if category not in category_totals:
        category_totals[category] = 0

    category_totals[category] += amount


total_expense = sum(expenses)
average_expense = total_expense / len(expenses)

highest_category = ""
lowest_category = ""
max_spend = -1
min_spend = float("inf")

for cat, amt in category_totals.items():
    if amt > max_spend:
        max_spend = amt
        highest_category = cat
    if amt < min_spend:
        min_spend = amt
        lowest_category = cat


if average_expense <= 200:
    status = "Controlled Spending"
elif average_expense <= 400:
    status = "Moderate Spending"
else:
    status = "High Spending"


print("\n=====================================")
print("        ADVANCED EXPENSE REPORT")
print("=====================================")
print("Expenses Entered        :", expenses)
print("Total Expense           :", total_expense)
print("Average Expense         :", round(average_expense, 2))
print("High Expense Entries    :", high_expense_count)

print("\nCategory-wise Breakdown:")
for cat, amt in category_totals.items():
    print(f"{cat:<10} : {amt}")

print("\nHighest Spending Category :", highest_category)
print("Lowest Spending Category  :", lowest_category)
print("Spending Status           :", status)
print("=====================================")
