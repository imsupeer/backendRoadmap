import unittest
from unittest.mock import patch
from src import number_guessing_game


class TestNumberGuessingGame(unittest.TestCase):
    @patch("src.number_guessing_game.random.randint")
    @patch("src.number_guessing_game.input")
    @patch("src.number_guessing_game.print")
    @patch("src.number_guessing_game.time.time")
    def test_win_round(self, mock_time, mock_print, mock_input, mock_randint):
        mock_randint.return_value = 30

        mock_input.side_effect = [
            "2",
            "50",
            "25",
            "30",
            "n",
        ]
        mock_time.side_effect = [1000.0, 1005.0]

        number_guessing_game.main()

        outputs = [call_arg[0][0] for call_arg in mock_print.call_args_list]
        self.assertTrue(
            any(
                "Congratulations! You guessed the correct number" in out
                for out in outputs
            )
        )

    @patch("src.number_guessing_game.random.randint")
    @patch("src.number_guessing_game.input")
    @patch("src.number_guessing_game.print")
    def test_lose_round(self, mock_print, mock_input, mock_randint):
        mock_randint.return_value = 70
        mock_input.side_effect = [
            "3",
            "30",
            "80",
            "60",
            "n",
        ]

        number_guessing_game.main()

        outputs = [call_arg[0][0] for call_arg in mock_print.call_args_list]
        self.assertTrue(any("You ran out of chances" in out for out in outputs))
        self.assertTrue(any("The correct number was 70" in out for out in outputs))


if __name__ == "__main__":
    unittest.main()
