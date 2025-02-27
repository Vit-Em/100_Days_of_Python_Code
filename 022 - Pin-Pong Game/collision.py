# collision.py
class CollisionManager:
    def __init__(self, ball, r_paddle, l_paddle):
        self.ball = ball
        self.r_paddle = r_paddle
        self.l_paddle = l_paddle

    def check_collisions(self):
        """Check if the ball collides with paddles."""
        # Check collision with the right paddle
        if self.ball.distance(self.r_paddle) < 50 and self.ball.xcor() > 340:
            self.ball.bounce_x()

        # Check collision with the left paddle
        if self.ball.distance(self.l_paddle) < 50 and self.ball.xcor() < -340:
            self.ball.bounce_x()
