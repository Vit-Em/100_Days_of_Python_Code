import time
from turtle import Screen

import scoreboard
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

def main():
    GameOn = True

    screen = Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)

    player = Player()
    car_manager = CarManager()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkey(player.go_up, "Up")
    screen.onkey(player.go_down, "Down")

    while GameOn:
        time.sleep(0.1)
        screen.update()

        car_manager.create_car()
        car_manager.move_cars()

        # collision with a car
        for car in car_manager.all_cars:
            if car.distance(player) < 20:
                GameOn = False
                scoreboard.game_over()

        # successful ending
        if player.is_at_finish_line():
            player.go_to_start()
            car_manager.level_up()
            scoreboard.increase_level()

    screen.exitonclick()

if __name__ == "__main__":
    main()
