# game_screen.py
from turtle import Screen, Turtle


class GameScreen:
    def __init__(self):
        """Initializes the game screen."""
        self.screen = Screen()  # Turtle's screen instance
        self.setup_screen()
        self.draw_middle_line()  # Draws dashed line at the middle of the screen
        self.text_turtle = Turtle()  # Turtle specifically for drawing text
        self.text_turtle.hideturtle()
        self.text_turtle.penup()
        self.text_turtle.color("white")

    def setup_screen(self):
        """Sets up the screen with size, background color, and title."""
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("black")
        self.screen.title("Pong Game")
        self.screen.tracer(0)  # Disable automatic screen updates for better control

    def draw_middle_line(self):
        """
        Draws a dashed white line in the middle of the game screen.
        Starts at the top (0, 300) and ends at the bottom (0, -300).
        """
        middle_line = Turtle()
        middle_line.hideturtle()
        middle_line.color("white")
        middle_line.penup()
        middle_line.goto(0, 300)  # Start at the top of the screen
        middle_line.setheading(270)  # Point downward
        while middle_line.ycor() > -300:
            middle_line.pendown()
            middle_line.forward(20)  # Draw segment of the dashed line
            middle_line.penup()
            middle_line.forward(20)  # Space to create a dashed effect

    def draw_score_underline(self):
        """
        Draws a straight white underline below the scoreboard area.
        Goes from (-20, 240) to (20, 240).
        """
        score_underline = Turtle()
        score_underline.hideturtle()
        score_underline.color("white")
        score_underline.penup()
        score_underline.goto(-20, 240)  # Start position below the scoreboard
        score_underline.setheading(0)  # Point to the right
        while score_underline.xcor() < 20:
            score_underline.pendown()
            score_underline.forward(40)
            score_underline.penup()

    def write(self, text, align="center", font=("Courier", 24, "normal")):
        """
        Displays text at the center of the screen.

        :param text: Text to display.
        :param align: Alignment of the text (e.g., 'center').
        :param font: Font type and size.
        """
        self.text_turtle.clear()  # Clear any previous text
        self.text_turtle.goto(0, 0)  # Center position
        self.text_turtle.write(text, align=align, font=font)

    def clear(self):
        """Clears any text displayed using `text_turtle`."""
        self.text_turtle.clear()

    def listen(self):
        """Enables the screen to listen for keyboard input."""
        self.screen.listen()

    def onkey(self, fun, key):
        """
        Binds a function to a specific key press.

        :param fun: Function to trigger when the key is pressed.
        :param key: Key to watch for.
        """
        self.screen.onkey(fun, key)

    def update(self):
        """Updates the screen."""
        self.screen.update()

    def exitonclick(self):
        """Exits the window when the user clicks on the game window."""
        self.screen.exitonclick()

    def bye(self):
        """Closes the Turtle window."""
        self.screen.bye()
