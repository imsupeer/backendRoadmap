import argparse
import json
import os
from datetime import date

EXPENSES_FILE = os.getenv(
    "EXPENSES_FILE",
    os.path.join(os.path.dirname(__file__), "..", "data", "expenses.json"),
)


def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
        try:
            expenses = json.load(f)
        except json.JSONDecodeError:
            expenses = []
    return expenses


def save_expenses(expenses):
    os.makedirs(os.path.dirname(EXPENSES_FILE), exist_ok=True)
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)


def get_next_id(expenses):
    if expenses:
        return max(expense["id"] for expense in expenses) + 1
    return 1


def add_expense(description, amount):
    expenses = load_expenses()
    expense_id = get_next_id(expenses)
    expense = {
        "id": expense_id,
        "date": date.today().isoformat(),
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense_id})")


def update_expense(expense_id, description, amount):
    expenses = load_expenses()
    found = False
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["description"] = description
            expense["amount"] = amount
            expense["date"] = date.today().isoformat()
            found = True
            break
    if found:
        save_expenses(expenses)
        print(f"Expense {expense_id} updated successfully.")
    else:
        print(f"Expense with ID {expense_id} not found.")


def delete_expense(expense_id):
    expenses = load_expenses()
    new_expenses = [expense for expense in expenses if expense["id"] != expense_id]
    if len(new_expenses) == len(expenses):
        print(f"Expense with ID {expense_id} not found.")
    else:
        save_expenses(new_expenses)
        print("Expense deleted successfully")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    print("ID  Date       Description  Amount")
    for expense in expenses:
        print(
            f"{expense['id']}   {expense['date']}  {expense['description']}  ${expense['amount']}"
        )


def summary(month=None):
    expenses = load_expenses()
    if month is not None:
        total = sum(
            expense["amount"]
            for expense in expenses
            if int(expense["date"].split("-")[1]) == month
        )
        import calendar

        month_name = calendar.month_name[month]
        print(f"Total expenses for {month_name}: ${total}")
    else:
        total = sum(expense["amount"] for expense in expenses)
        print(f"Total expenses: ${total}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add an expense")
    parser_add.add_argument("--description", required=True, help="Expense description")
    parser_add.add_argument(
        "--amount", required=True, type=float, help="Expense amount"
    )

    parser_update = subparsers.add_parser("update", help="Update an expense")
    parser_update.add_argument("--id", required=True, type=int, help="Expense ID")
    parser_update.add_argument("--description", required=True, help="New description")
    parser_update.add_argument("--amount", required=True, type=float, help="New amount")

    parser_delete = subparsers.add_parser("delete", help="Delete an expense")
    parser_delete.add_argument("--id", required=True, type=int, help="Expense ID")

    parser_list = subparsers.add_parser("list", help="List all expenses")

    parser_summary = subparsers.add_parser("summary", help="Show expense summary")
    parser_summary.add_argument(
        "--month", type=int, help="Month number (1-12) for filtering summary"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary(args.month)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
