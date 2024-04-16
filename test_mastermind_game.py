"""Daniela A. Gonzalez
CS5001- Mastermind
Tests"""

"""This class uses the unittest module in Python to
perform tests on functions related to the logic of
the game.

TestIsInvalidRow: Contains tests for the is_invalid_row
 function, evaluating cases of valid and invalid rows in a set.

TestCheckGuess: Different guesses scenarios are tested here
in relation to a check_guess function that evaluates whether
a color guess matches a secret code.

TestUserGame: This class performs a game simulation by calling 
the play_game function. It simulates 10 games, each with a 
maximum limit of attempts. It prints information about the 
progress of the game and evaluates the final result, verifying 
if the game ends correctly or continues depending on the guesses 
made and the score obtained.

When running the script, unittest.main() is used to run all 
the tests defined in the classes and check if they pass successfully.
If all tests pass, it will print "All tests passed!"."""


import unittest
from GameLogic import (
    check_guess,
    is_invalid_row,
    generate_secret_code,
    update,
    get_score,
    reset,
)


class TestIsInvalidRow(unittest.TestCase):
    def test_valid_row(self):
        """Function : test_valid_row.
         Test function to validate a row (no empty columns).
         Parameter: self.
        Return:
        - result (bool): Result of evaluating the row using the is_invalid_row function.
        Expects the valid row to return False.
        """""
        # Test a valid row (no empty columns)
        valid_row = ["red", "yellow", "gray", "blue"]
        result = is_invalid_row(valid_row)
        self.assertFalse(result, "Expected valid row to return False")

    def test_invalid_row(self):
        """Function : test_invalid_row.
         Test function to check an invalid row (contains empty columns).
         Parameter: self.
        Return:
        - result (bool): Result of evaluating the row using the is_invalid_row function.
        Expects the invalid row to return False.
        """""
        # Test an invalid row (contains empty columns)
        invalid_row = ["red", "", "gray", "blue"]
        result = is_invalid_row(invalid_row)
        self.assertTrue(result, "Expected invalid row to return True")


class TestCheckGuess(unittest.TestCase):
    def setUp(self):
        """Function: setUp.
        Setup established an environment to be tested
        establishing the variables in it
         Parameter: self 
         Return: none"""
        global gameover, current_row, code
        gameover = False
        current_row = 1
        code = ["red", "yellow", "gray", "blue"]

    def test_valid_guess_winning(self):
        """
        Function: test_valid_guess_winning.
        Test function to validate a winning guess.
        Validates a scenario where a valid guess leads to winning.
        Parameter:
        -self
    """

        colors_current_row = ["red", "yellow", "gray", "blue"]

        # Test a valid guess that leads to winning
        result, feedback = check_guess(colors_current_row, code)

        self.assertTrue(result, "Expected check guess to return True")
        self.assertEqual(
            feedback, ["black"] * len(code), "Expected feedback to have all black"
        )

    def test_invalid_guess(self):
        colors_current_row = ["red", "yellow", "green", "blue"]

        # Test an invalid guess
        result, feedback = check_guess(colors_current_row, code)

        self.assertFalse(result, "Expected check guess to return False")
        self.assertNotEqual(
            feedback, ["black"] * len(code), "Expected feedback to not have all black"
        )


class TestUserGame(unittest.TestCase):
    """
    Test class for user gameplay functionality.
    """
    @staticmethod
    def play_game(secret_code, colors, max_tries):
        """Function: play_game.
        Parameters:
        - secret_code (list)
        - colors(list)
        - max_tries (int)
        Returns:
        - win(bool)
        - result (dict)
        scorre (int)
        """
        reset()
        for i in range(max_tries):
            colors_current_row = generate_secret_code(colors, 4)
            win, feedback = check_guess(colors_current_row, secret_code)

            if win:
                result = {
                    "correctPosition": feedback.count("black"),
                    "incorrectPosition": feedback.count("red"),
                }
                update()
                print(f"Current try ({i+1}): {result}\n")
                print("You win!\n")
                break
            else:
                update()
                result = {
                    "correctPosition": feedback.count("black"),
                    "incorrectPosition": feedback.count("red"),
                }
                print(f"Current try ({i+1}): {result}\n")
        score = get_score()
        return win, result, score

    def test_play_game(self):
        """function: test_play_game.
        Parameters:
        -self"""
        colors = ["red", "blue", "green", "yellow", "purple", "black"]
        GAMES = 10
        MAX_TRIES = 10

        for game in range(GAMES):
            print(f"\n *** Game {game+1} *** \n")
            code = generate_secret_code(colors, 4)
            win, result, score = self.play_game(code, colors, MAX_TRIES)

            if result["correctPosition"] == 4:
                self.assertTrue(win, "Expected the game to be over")
                self.assertTrue(score > 0, "Expected a positive score for a win")
            else:
                self.assertTrue(not win, "Expected the game to continue for a loss")
                self.assertEqual(
                    score, MAX_TRIES, "Expected the maximum score for a loss"
                )


if __name__ == "__main__":
    # Run the tests
    unittest.main()

    print("All tests passed!")
