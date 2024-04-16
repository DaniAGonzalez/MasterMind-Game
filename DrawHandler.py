"""Daniela Gonzalez
CS5001
DrawHandler - MasterMind Project"""


import turtle
from time import sleep
from FileHandler import FileHandler

"""In this file I defined the Class Drawing Utilities 
for any draw that my Turtle is gonna be doing"""


class DrawingUtilities:
    def __init__(self, color="", pensize=0, position=(0, 0)):
        """
        Function: __init__(constuctor)
        Parameters:
        - color (str): Color of the turtle
        - pensize (int): Size of the turtle's pen
        - position (tuple): Initial position of the turtle
        """
        self.turtle = turtle.Turtle()
        self.setup_turtle(color, pensize, position)
        self.turtle.penup()

    def setup_turtle(self, color, pensize, position):
    
        """
        Function: setup_turtle.
        Set up a turtle definiying its speed,
        color and pen size.
        Parameters:
        - color (str): Color of the turtle
        - pensize (int): Size of the turtle's pen
        - position (tuple): Initial position of the turtle
        """
        self.turtle.ht()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.color(color)
        self.turtle.pensize(pensize)
        self.turtle.goto(position)

    def fill_color(self, color):
        """Function: fill_color.
          Setting up the turtle color
          Parameters: self, color(str)"""
        self.turtle.fillcolor(color)
        self.turtle.penup()

    def draw_title(self, text, font=("Arial Black", 25, "bold")):
        """
        Function: draw_title.
        Draw a title.
        Parameters:
        - text (str): The text of the title
        - font (tuple): The font of the title
        """
        self.turtle.write(text, align="left", font=font)
        self.turtle.penup()

    def draw_circle(self, x, y, radius, color=""):
        """
        Function: draw_circle.
        Draw a circle.

        Parameters:
        - x (int): The x-coordinate of the circle center
        - y (int): The y-coordinate of the circle center
        - radius (int): The radius of the circle
        """
        self.turtle.goto(x, y)
        self.turtle.pendown()
        # If there is no color, no need of painting them because the circles first are empty
        if color != "":
            self.turtle.fillcolor(color)
            self.turtle.begin_fill()

        self.turtle.circle(radius)

        if color != "":
            self.turtle.end_fill()

        self.turtle.penup()

    def draw_main_circles(self, rows, columns, radius):
        """
        Function: draw_main_circles
        Draws a grid of circles.

        Parameters:
        - rows (int): The number of rows in the grid.
        - columns (int): The number of columns in the grid.
        - radius (int): The radius of each circle.

        Returns:
        - circles (list): A matrix of dictionaries
                          with the information of the circles.
        """
        x_line = -120
        y_line = 240

        circles = [
            [None] * columns for _ in range(rows)
        ]  # Initialize a 2D list for circles

        for row in range(rows):
            for column in range(columns):
                self.draw_circle(x_line, y_line, radius)

                # Store information about the current circle in the matrix
                circle_info = {
                    "x": x_line,
                    "y": y_line,
                    "radius": radius,
                    "row": row,
                    "column": column,
                    "filled": False,
                    "color": "",
                }
                circles[row][column] = circle_info

                x_line += 50

            x_line = -120
            y_line -= 50

        return circles

    def draw_indicator_circles(self, rows, radius):
        """
        Function: draw_indicator_circles
        Draws the indicator circles (small ones)
        Indicator circles are the ones to
        provide feedback.

        Parameters:
        - rows (int): The number of rows in the grid.
        - radius (int): The radius of each circle.

        Returns:
        - indicator_circles (list): A matrix of dictionaries
                                    with the information of the circles.
        """
        y_small = 260

        indicator_circles = []

        for _ in range(rows):
            row_circles = []

            for _ in range(1):
                self.draw_circle(70, y_small, radius)
                self.draw_circle(90, y_small, radius)
                self.draw_circle(70, y_small - 20, radius)
                self.draw_circle(90, y_small - 20, radius)

                circle_info_1 = {
                    "x": 70,
                    "y": y_small,
                    "radius": radius,
                    "filled": False,
                    "color": "",
                }
                row_circles.append(circle_info_1)

                circle_info_2 = {
                    "x": 90,
                    "y": y_small,
                    "radius": radius,
                    "filled": False,
                    "color": "",
                }
                row_circles.append(circle_info_2)

                circle_info_3 = {
                    "x": 70,
                    "y": y_small - 20,
                    "radius": radius,
                    "filled": False,
                    "color": "",
                }
                row_circles.append(circle_info_3)

                circle_info_4 = {
                    "x": 90,
                    "y": y_small - 20,
                    "radius": radius,
                    "filled": False,
                    "color": "",
                }
                row_circles.append(circle_info_4)

                y_small -= 50

            indicator_circles.append(row_circles)

        return indicator_circles

    def draw_colored_circles(self, colors, radius):
        """
        Function: draw_colored_circles
        Draw circles with specified colors.

        Parameters:
        - colors (list): Colors for the circles
        - radius (int): The radius of the circles

        Returns:
        - circle_info_list (list): List of dictionaries
                                   representing circle information
        """
        y_col = 170
        circle_info_list = []

        for color in colors:
            self.turtle.goto(150, y_col)
            self.turtle.fillcolor(color)
            self.turtle.begin_fill()
            self.draw_circle(150, y_col, radius)
            self.turtle.end_fill()

            # Define the information for the current circle
            circle_info = {
                "x": 150,
                "y": y_col,
                "radius": radius,
                "filled": True,
                "color": color,
            }
            circle_info_list.append(circle_info)

            y_col -= 50

        return circle_info_list

    def redraw_row(self, row, circle_matrix):
        """
        Function: redraw_row
        Redraws the corresponding circles of a row.

        Parameters:
        - row (int): The row number to be redrawn.
        - circle_matrix (list): Information about each circle.
        """
        for column in range(len(circle_matrix[row])):
            circle_info = circle_matrix[row][column]
            circle_x = circle_info["x"]
            circle_y = circle_info["y"]
            circle_radius = circle_info["radius"]

            self.draw_circle(circle_x, circle_y, circle_radius, color="white")

    def draw_feedback(self, feedback, row, indicator_circles):
        """
        Function: draw_feedback
        Draw feedback circles with the indicated colour based on the 
        feedback list.

        Parameters:
        - feedback: A list of strings indicating the color.
        - row: The row number to draw the feedback circles.
        - indicator_circles: Information about each indicator circle.
        """
        radius = 5

        for i, color in enumerate(feedback):
            x = indicator_circles[row][i]["x"]
            y = indicator_circles[row][i]["y"]

            if color == "black":
                feedback_color = "black"
            elif color == "red":
                feedback_color = "red"
            else:
                feedback_color = "white"

            self.draw_circle(x, y, radius, feedback_color)


    def draw_panel(self, title, x, y, width=200, height=400): 
        """
        Function: draw_panel. 
        Draw a panel with its title.

        Parameters:
        - title(str): Title of the panel
        - x (int)
        - y (int)
        - width (int): Width of the panel
        - height (int): Height of the panel
        """
        self.turtle.goto(x, y)
        self.turtle.pendown()

        self.turtle.fillcolor("lightgray")
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(width)
            self.turtle.right(90)
            self.turtle.forward(height)
            self.turtle.right(90)
        self.turtle.end_fill()
        self.turtle.penup()

        # Display the title
        self.turtle.goto(x - 15, y + 5)
        self.draw_title(title)
        self.turtle.penup()

    def draw_leaderboard_panel(self, filename, color_circles_matrix):
        """
        Function: draw_leaderboard_panel. 
        Draw leaderboard.

        Parameters:
        - self
        - filename (file)
        - color_circles_matrix (list)
        """

        # Open the File for leaderboard 
        if not color_circles_matrix:
            print("Error: color_circles_matrix is empty.")
            return

        leaderboard_data = []
        user_score = []
        show_msg = "NO"
        title = "Leaderboard"
        x = color_circles_matrix[0]["x"] + 80
        y = 245
        width = 200
        height = len(color_circles_matrix) * 60 + 70

        self.draw_panel(title, x, y, width, height)

        try:
            fh = FileHandler()
            leaderboard_data, show_msg = fh.read_leaderboard(filename)
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating a new file.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.turtle.goto(x + 10, y - 20)

        for data in leaderboard_data:
            user_score.append((data["username"], data["score"]))

        # Sort list based on index 1 (user: index 0, score: index 1)
        user_score = sorted(user_score, key=lambda score: score[1])

        for user, score in user_score:
            self.turtle.color("black")
            self.turtle.write(
                f"{user}: {score}",
                align="left",
                font=("Arial", 10, "bold"),
                move=False,
            )
            self.turtle.goto(self.turtle.xcor(), self.turtle.ycor() - 15)

        self.turtle.penup()
        return show_msg

    def draw_instructions_panel(self, filename):
        """Function: draw_instructions_panel.
         Draw instructions.
        Writte the instructions in the panel
         Parameters: self, filename (file) """
        instructions = ""
        title = "How to play"
        x = -550
        y = 230
        width = 330
        height = 500

        self.draw_panel(title, x, y, width, height)

        try:
            fh = FileHandler()
            instructions = fh.read_instructions(filename)
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating a new file.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.turtle.goto(self.turtle.xcor() + 20, self.turtle.ycor() - 120)
        self.turtle.color("black")
        if instructions:
            self.turtle.write(
                instructions,
                align="left",
                font=("Arial", 10, "bold"),
                move=False,
            )
        else:
            self.turtle.write(
                """Instructions file lost!\nPlease try again.""",
                align="left",
                font=("Arial", 10, "bold"),
                move=False,
            )

        self.turtle.penup()
