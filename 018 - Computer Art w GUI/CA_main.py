import sys
import random
import turtle as t
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab, Image, ImageOps


# Turtle setup
screen = t.Screen()
screen.setup(600, 600)
screen.title("10x10 Dot Matrix - Meandering Path")
t.colormode(255)

tim = t.Turtle()
tim.speed("fastest")

# Define color palette
color_list = [(205, 143, 38), (46, 202, 144), (202, 164, 139), (240, 245, 201),
              (236, 209, 243), (149, 75, 50), (212, 201, 136), (53, 93, 123),
              (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73),
              (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70),
              (212, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77),
              (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129),
              (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153),
              (176, 192, 208), (168, 99, 102)]

# Choose random background color
background_color = random.choice(color_list)
screen.bgcolor(background_color)

# Prepare turtle
tim.penup()
tim.hideturtle()
start_x, start_y = -225, 225  # Starting position for centered matrix
tim.goto(start_x, start_y)

# Matrix parameters
rows, columns = 10, 10
dot_size = 20
spacing = 50

# Draw matrix with meandering path
for row in range(rows):
    for column in range(columns):
        # Choose random dot color
        dot_color = random.choice(color_list)
        while dot_color == background_color:
            dot_color = random.choice(color_list)

        # Draw dot
        tim.dot(dot_size, dot_color)

        # Move forward only if not at end of row
        if column < columns - 1:
            tim.forward(spacing)

    # Next row (meandering)
    if row < rows - 1:
        if row % 2 == 0:  # Even rows
            tim.right(90)
            tim.forward(spacing)
            tim.right(90)
        else:  # Odd rows
            tim.left(90)
            tim.forward(spacing)
            tim.left(90)


# Function to save the image
def save_screenshot():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if file_path:
        x = t.Screen().getcanvas().winfo_rootx()
        y = t.Screen().getcanvas().winfo_rooty()
        width = t.Screen().getcanvas().winfo_width()
        height = t.Screen().getcanvas().winfo_height()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(file_path)
        print(f"Screenshot saved as {file_path}")

def exit_program():
    print("Exiting program...")
    screen.bye()
    sys.exit(0)

# Save screenshot
save_screenshot()

# Set up exit on click if save dialog is cancelled
screen.onclick(lambda x, y: exit_program())
screen.mainloop()
