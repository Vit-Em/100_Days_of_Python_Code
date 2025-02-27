# paddle.py
from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position, is_pc=False):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(stretch_wid=6, stretch_len=1)
        self.goto(position)
        self.is_pc = is_pc

    def go_up(self):
        """Move the paddle up quickly."""
        if not self.is_pc:
            new_y = self.ycor() + 40  # Faster movement speed
            if new_y + 60 <= 300:  # Boundary limit (screen top: 300, considering paddle height -60)
                self.goto(self.xcor(), new_y)

    def go_down(self):
        """Move the paddle down quickly."""
        if not self.is_pc:
            new_y = self.ycor() - 40  # Faster movement speed
            if new_y - 60 >= -300:  # Boundary limit
                self.goto(self.xcor(), new_y)

    def pc_follow_ball(self, ball):
        """Make the computer-controlled paddle follow the ball."""
        if self.ycor() < ball.ycor() and self.ycor() < 250:  # Move up towards the ball
            self.goto(self.xcor(), self.ycor() + 20)
        elif self.ycor() > ball.ycor() and self.ycor() > -250:  # Move down towards the ball
            self.goto(self.xcor(), self.ycor() - 20)
