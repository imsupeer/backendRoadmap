import os
import tempfile
import shutil
import unittest
from unittest.mock import patch
from src import expense_tracker


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.expenses_file = os.path.join(self.temp_dir, "expenses.json")
        expense_tracker.EXPENSES_FILE = self.expenses_file

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch("builtins.print")
    def test_add_expense(self, mock_print):
        expense_tracker.add_expense("Lunch", 20)
        mock_print.assert_called_with("Expense added successfully (ID: 1)")
        expenses = expense_tracker.load_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Lunch")
        self.assertEqual(expenses[0]["amount"], 20)

    @patch("builtins.print")
    def test_update_expense_success(self, mock_print):
        expense_tracker.add_expense("Dinner", 15)
        expense_tracker.update_expense(1, "Dinner Updated", 18)
        mock_print.assert_called_with("Expense 1 updated successfully.")
        expenses = expense_tracker.load_expenses()
        self.assertEqual(expenses[0]["description"], "Dinner Updated")
        self.assertEqual(expenses[0]["amount"], 18)

    @patch("builtins.print")
    def test_update_expense_not_found(self, mock_print):
        expense_tracker.update_expense(99, "Nonexistent", 10)
        mock_print.assert_called_with("Expense with ID 99 not found.")

    @patch("builtins.print")
    def test_delete_expense_success(self, mock_print):
        expense_tracker.add_expense("Snack", 5)
        expense_tracker.delete_expense(1)
        mock_print.assert_called_with("Expense deleted successfully")
        expenses = expense_tracker.load_expenses()
        self.assertEqual(len(expenses), 0)

    @patch("builtins.print")
    def test_delete_expense_not_found(self, mock_print):
        expense_tracker.delete_expense(99)
        mock_print.assert_called_with("Expense with ID 99 not found.")

    @patch("builtins.print")
    def test_list_expenses(self, mock_print):
        expense_tracker.add_expense("Lunch", 20)
        expense_tracker.add_expense("Dinner", 10)
        expense_tracker.list_expenses()
        calls = [call_arg[0][0] for call_arg in mock_print.call_args_list]
        self.assertTrue(
            any("ID  Date       Description  Amount" in call for call in calls)
        )
        self.assertTrue(any("Lunch" in call for call in calls))
        self.assertTrue(any("Dinner" in call for call in calls))

    @patch("builtins.print")
    def test_summary_all(self, mock_print):
        expense_tracker.add_expense("Expense1", 30)
        expense_tracker.add_expense("Expense2", 20)
        expense_tracker.summary()
        mock_print.assert_called_with("Total expenses: $50")

    @patch("builtins.print")
    def test_summary_month(self, mock_print):
        current_month = int(expense_tracker.date.today().month)
        expense_tracker.add_expense("Expense1", 40)
        expense_tracker.summary(current_month)
        import calendar

        month_name = calendar.month_name[current_month]
        mock_print.assert_called_with(f"Total expenses for {month_name}: $40")


if __name__ == "__main__":
    unittest.main()
