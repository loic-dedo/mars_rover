from random import choices, randint

from rover import ConsoleDisplayer, Map, Rover

if __name__ == "__main__":
    map_instance = Map(30, 30)
    map_instance.generate_obstacles(obstacle_ratio=0.05)
    allowed_directions = ["N", "E", "S", "W"]
    allowed_commands = ["f", "b", "l", "r"]
    direction = allowed_directions[randint(0, 3)]
    mars_rover = Rover((randint(5, 25), randint(5, 25)), direction, map_instance)
    console_displayer = ConsoleDisplayer(map_instance)
    mars_rover.add_observer(console_displayer)
    n_commands = 1000
    commands = "".join(
        choices(population=allowed_commands, weights=[60, 20, 15, 5], k=n_commands)
    )
    mars_rover.execute_commands(commands)
