"""Daniela A. Gonzalez
cs5001 - Mastermind game
WindowHandler.py"""

"""WindowUtilities provides utilities for manipulating windows 
and displaying messages using the Turtle library in Python. 
A brief description of its main methods:
__init__: Initializes the window with a specified title, 
background color, width, and height.
register_shape: Registers new shapes (images) to be 
used by the turtle in the window.
bye: Closes the window.
show_message: Displays an image as a popup message in 
the window for 2 seconds, using the specified image path.
The class uses the turtle library to manipulate the window 
and display shapes and images in it."""

import turtle
from time import sleep

class WindowUtilities:
    def __init__(self, title="", color="", widht=0, height=0):
        """
        Parameters:
        - color (str): Color of the turtle
        - title (str): Title of the turtle
        - position (tuple): Initial position of the turtle
        """
        self.turtle = turtle.Screen()
        self.turtle.title(title)
        self.turtle.bgcolor(color)
        self.turtle.setup(widht, height)

    def register_shape(self, shape):
        """Function: register_shape.
        Register new shapes.
        Parameters:
        - shape: Shape to register
        """
        self.turtle.register_shape(shape)

    def bye(self):
        self.turtle.bye()

    @staticmethod
    def show_message(image_path):
        """
        Function: show_message.
        Shows an image like a popup
        Parameters:
        - image_path(str): The path to the image to show
        """
        img_turtle = turtle.Turtle()
        img_turtle.penup()
        img_turtle.shape(image_path)
        img_turtle.showturtle()
        sleep(2)
        img_turtle.ht() #hide 
