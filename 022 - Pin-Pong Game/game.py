# game.py
from game_screen import GameScreen
from paddle import Paddle
from ball import Ball
from collision import CollisionManager
from score import Score
from turtle import Turtle


class Game:
    def __init__(self):
        self.screen = GameScreen()
        self.r_paddle = None
        self.l_paddle = None
        self.ball = Ball()
        self.collision_manager = None
        self.score = Score()
        self.is_running = False  # Game state

    def show_start_menu(self):
        """Displays the start menu and waits for user input."""
        self.screen.clear()  # Clear the screen
        self.screen.write(
            "PING PONG GAME\n\n"
            "Press '1' for Single Player\n"
            "Press '2' for Multiplayer\n"
            "Press 'ESC' to Exit",
            align="center", font=("Courier", 24, "normal"))

        # Key bindings for the menu
        self.screen.listen()
        self.screen.onkey(self.select_single_player, "1")
        self.screen.onkey(self.select_multiplayer, "2")
        self.screen.onkey(self.exit_game, "Escape")

    def select_single_player(self):
        """Select single-player mode."""
        self.r_paddle = Paddle((380, 0))  # Right paddle: Player
        self.l_paddle = Paddle((-380, 0), is_pc=True)  # Left paddle: Controlled by PC
        self.start_game()

    def select_multiplayer(self):
        """Select multiplayer mode."""
        self.r_paddle = Paddle((380, 0))  # Right paddle: Player
        self.l_paddle = Paddle((-380, 0))  # Left paddle: Player
        self.start_game()

    def start_game(self):
        """Initialize game components and start the main game loop."""
        self.collision_manager = CollisionManager(self.ball, self.r_paddle, self.l_paddle)
        self.is_running = True
        self.screen.clear()  # Clear the start menu
        self.setup_controls()
        self.run_game_loop()

    def exit_game(self):
        """Exit the game."""
        self.is_running = False
        self.screen.bye()

    def setup_controls(self):
        """Set up paddle controls for the players."""
        self.screen.onkey(self.r_paddle.go_up, "Up")
        self.screen.onkey(self.r_paddle.go_down, "Down")
        if not self.l_paddle.is_pc:
            # Only for multiplayer mode
            self.screen.onkey(self.l_paddle.go_up, "w")
            self.screen.onkey(self.l_paddle.go_down, "s")

    def run_game_loop(self):
        """Main game loop."""
        if self.is_running:  # Only continue if the game is still running
            self.ball.move()

            # PC-controlled paddle follows the ball (if enabled for single-player mode)
            if self.l_paddle.is_pc:
                self.l_paddle.pc_follow_ball(self.ball)

            self.collision_manager.check_collisions()
            self.check_score()  # Check if a point is scored
            if self.is_running:  # Check again after updating scores to avoid updating a closed screen
                self.screen.update()
                self.screen.screen.ontimer(self.run_game_loop, 20)  # Schedule the next frame

    def check_score(self):
        """Check if a point has been scored."""
        if self.ball.xcor() > 390:  # Player scores
            self.score.l_point()
            self.ball.reset_position()

        if self.ball.xcor() < -390:  # PC or second player scores
            self.score.r_point()
            self.ball.reset_position()

        if self.score.is_game_over():  # Check if there is a winner
            winner = self.score.get_winner()
            self.score.display_winner(winner)
            self.is_running = False  # Stop the game loop
            self.screen.bye()  # Close the game window

    def play(self):
        """Start the game and display the start menu."""
        self.show_start_menu()
        while not self.is_running:  # Wait for user input in the menu
            self.screen.update()

        # Game is running
        self.screen.screen.mainloop()
