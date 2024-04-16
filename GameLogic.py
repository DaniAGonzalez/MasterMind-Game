"""
Daniela A. Gonzalez
Game Logic.
This file involves the functions related to the logic
of playing Mastermind 

"""


import turtle as t
from random import shuffle
from DrawHandler import DrawingUtilities
from FileHandler import FileHandler
from time import sleep

# Drafter positioning
dw = DrawingUtilities("grey", 0.5, (-150, -230)) 

score = 0
current_row = 0


def update():
    """
    Function update: Updates score and current_row

    """
    global score, current_row
    score += 1
    current_row += 1


def reset():
    """
    Function reset : set to zero both score
    and rows. Necessary to be used for the tests.
     """
    global score, current_row
    score = 0
    current_row = 0


def get_score():
    return score


# Username Set
def show_alert(message):
    """Function show_alert:
    Displays an alert message on the screen using Turtle graphics.
    Parameters:
    - message (str): The message to be displayed as an alert.
    Return: None
    """
    t.penup()
    t.goto(0, 0)
    t.color("red")
    t.write(message, align="center", font=("Arial", 16, "normal"))
    t.hideturtle()


def get_username():
    """Function get_unsername: 
    Prompts the user to input a username adhering to certain rules.
    Returns:
    - username (str): The valid username input by the user.
    """
    username = ""
    while username == "":
        username = t.textinput("Username Input", "Enter your username:")
        if len(username) <= 5 or username is None:
            # Alert message
            show_alert("The username len must be gratter than 5 characters.")
            username = ""

    t.clear()
    t.penup()
    t.hideturtle()
    return username


def update_score_file(window, filename, username, score):
    """
    Function update_score:
    Update the score for a given username in the specified file.

    Parameters:
        - window: WindowUtilities object
        - filename (str): The name of the file to update.
        - username (str): The username for which to set/update the score.
        - score (int): The new score to set.

        Raises:
        - Exception: If an error occurs during the update process.
    """
    try:
        fh = FileHandler()
        fh.update_score(filename, username, score)
    except Exception as e:
        window.show_message("file_error.gif")




def generate_secret_code(color_list, code_length=4):
    """
    Function generate_secret_code : Generate a 
    random secret code.

    Parameters:
        - color_list (list): Colours available.
        - code_length (int): Lenght of the secret code
    Return: secret code for colors
    """
    color_list_aux = color_list
    # Shuffle the color list to get a random order
    shuffle(color_list_aux)
    # Take the first 'code_length' elements
    secret_code = color_list[:code_length]
    return secret_code


def check_guess(colors_current_row, secret_code):
    """
    Function check_guess: Check if the current row 
    matches the secret code and provide feedback.

    Parameters:
    - colors_current_row: The colors of the current row to check
    - secret_code: The secret code to compare with

    Returns:
    - True if the current row matches the secret code, False otherwise
    """
    # reset feedback list each time
    feedback = []  

    # Check for correct color and position (black feedback)
    for i in range(len(secret_code)):
        if colors_current_row[i] == secret_code[i]:
            feedback.append("black")

    # Check for correct color but incorrect position (red feedback)
    for i in range(len(secret_code)):
        if (
            colors_current_row[i] != secret_code[i]
            and colors_current_row[i] in secret_code
        ):
            feedback.append("red")

    if feedback != ["black"] * len(secret_code):
        return False, feedback

    return True, feedback


def select_color(x, y, circle_info_list, circle_matrix):
    """
    
    Function select_color: Selects the color from the color palette based 
    on the given coordinates.

    Parameters:
    - x (int): The x-coordinate of the click.
    - y (int): The y-coordinate of the click.
    - circle_info_list (list): Information about each colored circle.
    - circle_matrix: List of dictionaries with info about main circles
    """
    for circle_info in circle_info_list:
        circle_x = circle_info["x"]
        circle_y = circle_info["y"]
        radius = circle_info["radius"] 
        color = circle_info["color"]

        if (
            circle_x - radius < x < circle_x + radius
            and circle_y - radius < y < circle_y + radius
        ): 
            dw.fill_color(color)
            fill_manager(circle_matrix, color)
            break
        


def fill_manager(circle_matrix, color):
    """
    Function fill_manager: Check if the circle is 
    not already filled and
    fills the correspondent circle.

    Parameters:
    - circle_matrix: List of dictionaries with info about main circles
    - color: Selected color to fill the empty circle.
    Return
    - none
    """
    global current_row

    for column in range(len(circle_matrix[current_row])):
        circle_info = circle_matrix[current_row][column]
        circle_filled = circle_info.get("filled", False)
        if not circle_filled:
            colors_current_row = get_current_row_colors(circle_matrix)
            if color and color in colors_current_row:
                return
            fill_circle(circle_info, color)
            circle_info["filled"] = True
            return 


def fill_circle(circle_info, color):
    """
    Function fill_circle: Update the color information in 
    the circle_info and
    redraw the circle with the updated color

    Parameters:
    - circle_info (list): Information about the circle to fill.
    - color (str): color to fill the circle
    Return
    -none
    """
    circle_info["color"] = color
    dw.draw_circle(
        circle_info["x"],
        circle_info["y"],
        circle_info["radius"],
        circle_info["color"],
    )


def is_invalid_row(row):
    """
    Function is_invalid_row:
    Check if the row is invalid.

    A row is invalid when has empty columns.

    Parameters:
    - row (List): Colours of each column
    """
    return any(not column for column in row)


def press_enter(window, x, y, code, indicator_circles, circle_matrix, username):
    """
    Fucntion press_enter:
    Submit button action.
    Manages the logic to decide if the user wins or not.
    Updates the user's score. If the user wins then update the scores file.
    If not change the row to the next.

    Parameters:
    - window: WindowUtilities object
    - x (int): The x-coordinate of the click.
    - y (int): The y-coordinate of the click.
    - feedback: A list of strings indicating the color.
    - indicator_circles: Information about each indicator circle.
    """
    submit_button_area = {"x_min": 132, "x_max": 184, "y_min": 219, "y_max": 276}

    if (
        submit_button_area["x_min"] < x < submit_button_area["x_max"]
        and submit_button_area["y_min"] < y < submit_button_area["y_max"]
    ):
        colors_current_row = get_current_row_colors(circle_matrix)

        if is_invalid_row(colors_current_row):
            return

        if check_guess(colors_current_row, code)[0]: #if true > gane
            feedback = check_guess(colors_current_row, code)[1]
            dw.draw_feedback(feedback, current_row, indicator_circles)
            window.show_message("winner.gif")
            update()
            try:
                update_score_file(window, "scores.txt", username, score)
            except Exception as e:
                window.show_message("file_error.gif")

            sleep(1)
            window.bye()
        else:
            update() #it increases the next line and add the score + 1. If we reach the last line we lost
            feedback = check_guess(colors_current_row, code)[1]
            dw.draw_feedback(feedback, current_row - 1, indicator_circles)
            if current_row == 10:
                window.show_message("Lose.gif")
                sleep(1)
                window.bye()


def get_current_row_colors(circle_matrix):
    """
    Function get_current_row_colors: Get the colours
     of the current row.

    Parameters:
    - circle_matrix: List of dictionaries with info about main circles

    Returns:
    - colors_current_row(list)
    """
    global current_row
    colors_current_row = []
    for column in range(len(circle_matrix[current_row])):
        colors_current_row.append(circle_matrix[current_row][column]["color"])

    return colors_current_row


def reset_row(x, y, circle_matrix):
    """
    Function reset_row: Reset row action.
    Redraw filled circles in a row making them empty
    to re-start the attempt on that row.

    Parameters:
    - x (int): The x-coordinate of the click.
    - y (int): The y-coordinate of the click.
    - circle_matrix: List of dictionaries with info about main circles
    """

    global current_row, gameover
    global dw

    reset_button_area = {"x_min": 134, "x_max": 189, "y_min": -177, "y_max": -230}

    if (
        reset_button_area["x_min"] < x < reset_button_area["x_max"]
        and reset_button_area["y_max"] < y < reset_button_area["y_min"]
    ):
        # Clear the filled status of each circle in the current row
        for column in range(len(circle_matrix[current_row])):
            circle_matrix[current_row][column]["filled"] = False
            circle_matrix[current_row][column]["color"] = ""

        dw.redraw_row(current_row, circle_matrix)


def quit_game(x, y, window):
    """
    Function quit_game:
    Quit button action.

    Parameters:
    - window: WindowUtilities object
    - x (int): The x-coordinate of the click.
    - y (int): The y-coordinate of the click.
    """

    submit_button_area = {"x_min": 237, "x_max": 424, "y_min": -218, "y_max": -320}
    if (
        submit_button_area["x_min"] < x < submit_button_area["x_max"]
        and submit_button_area["y_max"] < y < submit_button_area["y_min"]
    ):
        window.show_message("images" + "/quitmsg.gif")
        sleep(1)
        window.bye()

