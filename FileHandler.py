"""Daniela Alejandra Gonzalez
CS 5001- Mastermind game
Filehandler.py"""

from datetime import datetime

class FileHandler:
    @staticmethod
    def update_score(filename, username, score):
        """
        Function: update_score
        Update the score for a given username in the specified file.

        Parameters:
        - filename (str): The name of the file to update.
        - username (str): The username for which to set/update the score.
        - score (int): The new score to set.

        Raises:
        - Exception.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Find the line corresponding to the given username
            for i, line in enumerate(lines):
                if line.startswith(f"{username},"):
                    lines[i] = f"{username},{score}\n"
                    break
            else:
                # If the username is not found, add a new entry
                lines.append(f"{username},{score}\n")

            with open(filename, "w", encoding="utf-8") as file:
                file.writelines(lines)

        except FileNotFoundError:
            # If the file doesn't exist, create it
            FileHandler.write_error(
                "update_score",
                f"File '{filename}' not found. Creating a new file.",
                error_type="ReadError",
            )
            with open(filename, "w", encoding="utf-8") as file:
                file.write("# Leaderboard File\n# Format: username,score\n")

        except Exception as e:
            FileHandler.write_error(
                "update_score",
                f"Error updating score: {e}",
                error_type="UpdateError",
            )

    @staticmethod
    def read_leaderboard(filename):
        """
        Function: read_leaderboard
        Read the leaderboard data from the specified file.

        Parameters:
        - filename (str): The name of the file to read.

        Returns:
        - leaderboard_data (List): A list of dictionaries.

        Raises:
        - Exception.
        """
        leaderboard_data = []
        show_msg = "NO"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                # Skip header
                lines = file.readlines()[2:]  # Skip the first two lines
                # Read the existing leaderboard content
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        username, score = parts
                        leaderboard_data.append({"username": username, "score": score})
                    else:
                        FileHandler.write_error(
                            "read_leaderboard",
                            f"Invalid line in '{filename}': {line}",
                            error_type="ReadError",
                        )

        except FileNotFoundError:
            # If the file doesn't exist, create it
            FileHandler.write_error(
                "read_leaderboard",
                f"File '{filename}' not found. Creating a new file.",
                error_type="ReadError",
            )
            with open(filename, "w", encoding="utf-8") as file:
                file.write("# Leaderboard File\n# Format: username,score\n")

            show_msg = "yes"

        except Exception as e:
            FileHandler.write_error(
                "read_leaderboard",
                f"Error reading leaderboard: {e}",
                error_type="ReadError",
            )

        return leaderboard_data, show_msg

    @staticmethod
    def write_error(method_name, error_message, error_type="Unknown"):
        """
        Function: write_error.
        Write an error message to a log file.

        Parameters:
        - method_name (str): The name of the method where the error occurred.
        - error_message (str): The error message to log.
        - error_type (str): The type of the error.
        """
        try:
            with open("mastermind_errors.txt", "a", encoding="utf-8") as error_file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_file.write(
                    f"Error: {error_message}\nDescription: {method_name}\nType: {error_type}\nDate: {current_time}\n"
                )
                error_file.write("-" * 30 + "\n")  # Separator between entries
        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open("mastermind_errors.txt", "w", encoding="utf-8") as error_file:
                error_file.write("# Error Log\n")
        except Exception as e:
            print(f"Error writing to error log: {e}")

    @staticmethod
    def read_instructions(filename):
        """Method:read_instructions.
        Read a file with the instructions 
        to be put into the screen
        Parameters:
         - filename (file)
        Return:
         - instructions """
        instructions = ""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                instructions = file.read()
        except FileNotFoundError:
            # If the file doesn't exist, create it
            FileHandler.write_error(
                "read_instructions",
                f"File '{filename}' not found. Creating a new file.",
                error_type="ReadError",
            )
            with open(filename, "w", encoding="utf-8") as file:
                file.write(
                    """1. Select a colour from the color palette.
  to fill an empty circle.
3. Complete the row with different colors.
4. Once completed you can check the row.
5. If you want to 'restart' the row click the X button.
6. That's it. Enjoy!"""
                )

        except Exception as e:
            FileHandler.write_error(
                "read_intructions",
                f"Error reading instructions: {e}",
                error_type="ReadError",
            )

        return instructions
