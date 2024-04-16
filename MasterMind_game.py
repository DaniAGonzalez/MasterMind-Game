"""
Daniela A. Gonzalez
MasterMind game
"""


import turtle as t
from random import shuffle
from DrawHandler import DrawingUtilities
from WindowHandler import WindowUtilities
import GameLogic as gm


colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "black",
]


""" Canvas and Content Section """ 


def setup_button(shape_path, position, onclick_action, size=2):
    """
    Function: setup_button.
    Creates a button on the screen.

    Parameters:
    - shape_path (str): The path to the registered shape for the button.
    - position (tuple): The coordinates (x, y) where the button will be placed.
    - onclick_action (function): The action to be performed when the button is clicked.
    - size (int, optional): The size of the button. Defaults to 2.

    """

    button_turtle = t.Turtle()
    button_turtle.penup()
    button_turtle.goto(position)
    button_turtle.shape(shape_path)
    button_turtle.shapesize(stretch_wid=size, stretch_len=size, outline=1)
    button_turtle.onclick(lambda x, y: onclick_action(x, y)) 


def content_section(window, code):
    """
    Function: content_section
    Displays the main content section of the Mastermind game.

    Parameters:
    - window (object): The window object to display the game content.
    - code (list): The code used in the game for validation.

    Returns:
    - circle_matrix (list): Matrix representing the main circles of the game board.
    - color_circles_matrix (list): Matrix of colored circles used in the game.
    """
    username = gm.get_username()
    # Title
    title = DrawingUtilities("grey", 10, (-150, -280))
    title.draw_title("MASTERMIND")
    #Class to make draws
    dw = DrawingUtilities("grey", 0.5, (-150, -230))
    # How to play:
    instructions = DrawingUtilities("grey", 5, (-0, 0))
    instructions.draw_instructions_panel("instructions.txt")
    circle_matrix = dw.draw_main_circles(10, 4, 15)
    # Drawing Indicator Circles
    circle_feedback_matrix = dw.draw_indicator_circles(10, 5)
    # Check button
    setup_button(
        "checkbutton.gif",
        (160, 245),
        lambda x, y: gm.press_enter(
            window, x, y, code, circle_feedback_matrix, circle_matrix, username
        ),
    )
    # Reset button
    setup_button(
        "xbutton.gif",
        (160, -205),
        lambda x, y: gm.reset_row(x, y, circle_matrix),
    )
    # Quit button
    setup_button(
        "quit.gif", (330, -270), lambda x, y: gm.quit_game(x, y, window)
    )

    # Drawing colored circles
    color_list_aux = colors
    # Shuffle the color list to get a random order
    shuffle(color_list_aux)
    color_circles_matrix = dw.draw_colored_circles(color_list_aux, 15)

    # Leaderboard
    show_msg = dw.draw_leaderboard_panel("scores.txt", color_circles_matrix)

    if show_msg == "YES":
        window.show_message("file_error.gif")

    return circle_matrix, color_circles_matrix 


def clk(x, y, color_matrix, matrix):
    """Function: clk.
    Select a color in the color_matrix using the coordinates x and y.

    Parameters:
    - x (int).
    - y (int). 
    - color_matrix (list)
    - matrix (list)
    Returns:
    None
    """
    gm.select_color(x, y, color_matrix, matrix) #gm


def main():
    # WindowsUtilities is a class I defined to handle methods for windows
    wn = WindowUtilities("Mastermind", "white", 650, 400) 
    wn.register_shape("checkbutton.gif")  
    wn.register_shape("xbutton.gif") 
    wn.register_shape("winner.gif")
    wn.register_shape("Lose.gif")
    wn.register_shape("quit.gif")
    wn.register_shape("quitmsg.gif")
    wn.register_shape("file_error.gif")

    code = gm.generate_secret_code(
        colors,
        4,
    )

    matrix, color_matrix = content_section(wn, code)
    print(code)
    t.onscreenclick(lambda x, y: clk(x, y, color_matrix, matrix))


if __name__ == "__main__":
    main()
    # Listening to mouse click
    t.listen()
    t.done()
