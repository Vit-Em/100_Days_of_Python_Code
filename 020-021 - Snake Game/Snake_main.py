from turtle import Screen
from snake import Snake  # Snake class
from food import Food  # Food class
from scoreboard import Scoreboard  # Scoreboard class
import time
from tkinter import TclError

# Screen setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

# Create game objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# Keyboard bindings
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# Flag to track if the window is open
window_open = True


def close_window():
    """Gracefully handle window closure."""
    global window_open
    window_open = False  # Mark that the window is closed
    screen.bye()  # Close the window properly


# Bind the window close event
screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", close_window)

# Main game loop
while window_open:  # Run the game only while the window is open
    try:
        game_is_on = True
        while game_is_on:
            screen.update()  # Update the screen for each frame

            if not window_open:  # Stop the game if the window is closed
                break

            time.sleep(0.1)
            snake.move()

            # Detect collision with food
            if snake.head.distance(food) < 15:
                food.refresh()
                snake.extend()
                scoreboard.increase_score()

            # Detect collision with wall
            if (
                    snake.head.xcor() > 280
                    or snake.head.xcor() < -280
                    or snake.head.ycor() > 280
                    or snake.head.ycor() < -280
            ):
                game_is_on = False
                scoreboard.game_over()

            # Detect collision with tail
            for segment in snake.segments[1:]:
                if snake.head.distance(segment) < 10:
                    game_is_on = False
                    scoreboard.game_over()

        if window_open:  # Reset only if the window is still open
            scoreboard.clear_game_over()
            snake.reset()
            food.refresh()

    except (TclError, KeyboardInterrupt):
        # Gracefully handle window closure or a manual interrupt
        break  # Exit the loop

print("Game has been closed.")
