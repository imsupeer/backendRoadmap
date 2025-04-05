import unittest
from unittest.mock import patch, MagicMock
from src import task_tracker
from tests import mock_loader


class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        self.initial_task = mock_loader.from_json("mocks/test_tasks.json")
        self.updated_description = "Comprar mantimentos e preparar jantar"
        self.fake_now = "2025-04-04T00:00:00"

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("src.task_tracker.datetime")
    @patch("builtins.print")
    def test_add_task(
        self, mock_print, mock_datetime, mock_load_tasks, mock_save_tasks
    ):
        mock_load_tasks.return_value = []
        fake_now_obj = MagicMock()
        fake_now_obj.isoformat.return_value = self.fake_now
        mock_datetime.now.return_value = fake_now_obj

        task_tracker.add_task("Comprar mantimentos")

        mock_save_tasks.assert_called_once()
        tasks_arg = mock_save_tasks.call_args[0][0]
        self.assertEqual(len(tasks_arg), 1)
        self.assertEqual(tasks_arg[0]["description"], "Comprar mantimentos")
        self.assertEqual(tasks_arg[0]["status"], "todo")
        self.assertEqual(tasks_arg[0]["createdAt"], self.fake_now)
        self.assertEqual(tasks_arg[0]["updatedAt"], self.fake_now)

        mock_print.assert_called_once()
        self.assertIn("Tarefa adicionada com sucesso", mock_print.call_args[0][0])

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_update_task_success(self, mock_print, mock_load_tasks, mock_save_tasks):
        mock_load_tasks.return_value = [self.initial_task.copy()]

        task_tracker.update_task(1, self.updated_description)

        tasks_arg = mock_save_tasks.call_args[0][0]
        self.assertEqual(tasks_arg[0]["description"], self.updated_description)
        mock_print.assert_called_once_with("Tarefa 1 atualizada com sucesso.")

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_update_task_not_found(self, mock_print, mock_load_tasks, mock_save_tasks):
        mock_load_tasks.return_value = []
        task_tracker.update_task(99, self.updated_description)
        mock_print.assert_called_once_with("Tarefa com ID 99 não encontrada.")
        mock_save_tasks.assert_not_called()

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_delete_task_success(self, mock_print, mock_load_tasks, mock_save_tasks):
        mock_load_tasks.return_value = [self.initial_task.copy()]
        task_tracker.delete_task(1)
        mock_print.assert_called_once_with("Tarefa 1 deletada com sucesso.")
        tasks_arg = mock_save_tasks.call_args[0][0]
        self.assertEqual(len(tasks_arg), 0)

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_delete_task_not_found(self, mock_print, mock_load_tasks, mock_save_tasks):
        mock_load_tasks.return_value = []
        task_tracker.delete_task(99)
        mock_print.assert_called_once_with("Tarefa com ID 99 não encontrada.")
        mock_save_tasks.assert_not_called()

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_mark_task_status_in_progress_success(
        self, mock_print, mock_load_tasks, mock_save_tasks
    ):
        mock_load_tasks.return_value = [self.initial_task.copy()]
        task_tracker.mark_task_status(1, "in-progress")
        tasks_arg = mock_save_tasks.call_args[0][0]
        self.assertEqual(tasks_arg[0]["status"], "in-progress")
        mock_print.assert_called_once_with("Tarefa 1 marcada como in-progress.")

    @patch("src.task_tracker.save_tasks")
    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_mark_task_status_done_success(
        self, mock_print, mock_load_tasks, mock_save_tasks
    ):
        mock_load_tasks.return_value = [self.initial_task.copy()]
        task_tracker.mark_task_status(1, "done")
        tasks_arg = mock_save_tasks.call_args[0][0]
        self.assertEqual(tasks_arg[0]["status"], "done")
        mock_print.assert_called_once_with("Tarefa 1 marcada como done.")

    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_list_tasks_no_tasks(self, mock_print, mock_load_tasks):
        mock_load_tasks.return_value = []
        task_tracker.list_tasks()
        mock_print.assert_called_once_with("Nenhuma tarefa encontrada.")

    @patch("src.task_tracker.load_tasks")
    @patch("builtins.print")
    def test_list_tasks_with_tasks(self, mock_print, mock_load_tasks):
        mock_load_tasks.return_value = [self.initial_task.copy()]
        task_tracker.list_tasks()
        self.assertTrue(mock_print.call_count > 0)


if __name__ == "__main__":
    unittest.main()
