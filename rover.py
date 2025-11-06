from os import system
from random import sample
from time import sleep


class Map:
    def __init__(self, width: int, height: int, matrix: list[list[int]] = None):
        """
        The Map class represents a 2D grid map for the Rover to navigate.
        It's a sphere like map where moving beyond the edges wraps around.
        Each cell in the map can be 0 (empty) or 1 (obstacle).
        The map is initialized with no obstacles.
        :param width: Width of the map
        :param height: Height of the map
        """
        self.width: int = width
        self.height: int = height
        if matrix is not None:
            self.matrix = matrix
        else:
            self.matrix = [[0 for _ in range(width)] for _ in range(height)]

    def generate_obstacles(self, obstacle_ratio: float = 0.05):
        """
        Randomly generates obstacles on the map based on the given ratio.
        """
        total_cells = self.width * self.height
        n_obstacles = int(total_cells * obstacle_ratio)
        all_positions = [(x, y) for y in range(self.height) for x in range(self.width)]
        obstacle_positions = sample(all_positions, n_obstacles)
        for x, y in obstacle_positions:
            self.matrix[y][x] = 1

    def is_obstacle(self, x: int, y: int) -> bool:
        return self.matrix[y][x] == 1

    def wrap_position(self, x: int, y: int, direction: str) -> tuple[int, int, str]:
        if y < 0:  # Crossing North Pole
            y = self.height - 1
            direction = "N"
        elif y >= self.height:  # Crossing South Pole
            y = 0
            direction = "S"

        if x < 0:  # Crossing West Edge
            x = self.width - 1
        elif x >= self.width:  # Crossing East Edge
            x = 0

        return x, y, direction

    def replace_matrix(self, new_matrix: list[list[int]]):
        self.matrix = new_matrix


class Rover:
    """
    The Rover class represents a rover that can navigate on a 2D grid map.
    It can move forward, backward, and turn left or right.
    It does so by being provided with a list of commands.
    """

    def __init__(
        self, starting_point: tuple[int, int], direction: str, map_instance: Map
    ):
        self.x, self.y = starting_point
        self.direction = direction.upper()
        self._allowed_directions = ["N", "W", "S", "E"]
        self._map = map_instance
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, movement: str | None = None, event: str | None = None):
        for obs in self._observers:
            obs.update(self, movement, event)

    def move_forward(self) -> bool:
        """
        Moves the rover one unit forward in the direction it is currently facing.
        If the move would result in a collision with an obstacle:
        - The rover does not move.
        - A collision event is triggered.
        - Returns True if the move was successful, False otherwise.
        """
        new_x, new_y = self.x, self.y
        if self.direction == "N":
            new_y -= 1
        elif self.direction == "E":
            new_x += 1
        elif self.direction == "S":
            new_y += 1
        elif self.direction == "W":
            new_x -= 1
        new_x, new_y, new_direction = self._map.wrap_position(
            new_x, new_y, self.direction
        )
        if self._map.is_obstacle(new_x, new_y):
            self.notify_observers(movement="Forward", event="collision")
            return False
        self.x, self.y, self.direction = new_x, new_y, new_direction
        self.notify_observers(movement="Forward")
        return True

    def move_backward(self) -> bool:
        """
        Moves the rover one unit backward in the direction it is currently facing.
        If the move would result in a collision with an obstacle:
        - The rover does not move.
        - A collision event is triggered.
        - Returns True if the move was successful, False otherwise.
        """
        new_x, new_y = self.x, self.y
        if self.direction == "N":
            new_y += 1
        elif self.direction == "E":
            new_x -= 1
        elif self.direction == "S":
            new_y -= 1
        elif self.direction == "W":
            new_x += 1
        new_x, new_y, new_direction = self._map.wrap_position(
            new_x, new_y, self.direction
        )
        if self._map.is_obstacle(new_x, new_y):
            self.notify_observers(movement="Backward", event="collision")
            return False
        self.x, self.y, self.direction = new_x, new_y, new_direction
        self.notify_observers(movement="Backward")
        return True

    def turn_left(self):
        current_index = self._allowed_directions.index(self.direction)
        self.direction = self._allowed_directions[(current_index + 1) % 4]
        self.notify_observers(movement="Left")

    def turn_right(self):
        current_index = self._allowed_directions.index(self.direction)
        self.direction = self._allowed_directions[(current_index - 1) % 4]
        self.notify_observers(movement="Right")

    def execute_commands(self, commands: str):
        """
        Executes a sequence of commands to move the rover.
        Commands:
        - 'F': Move forward
        - 'B': Move backward
        - 'L': Turn left
        - 'R': Turn right
        If a move command results in a collision, the execution stops.
        :param commands: A string of commands
        """
        for command in commands:
            command = command.upper()
            if command == "F":
                if not self.move_forward():
                    break
            elif command == "B":
                if not self.move_backward():
                    break
            elif command == "L":
                self.turn_left()
            elif command == "R":
                self.turn_right()


class Displayer:
    """
    The Displayer class is an abstract base class for displaying the rover within a Map.
    It defines the interface for displayers and implements the observer pattern.
    Subclasses should override the display method to provide specific display functionality.
    """

    def __init__(self, map_instance: Map):
        self.map = map_instance

    def display(
        self, rover: Rover, movement: str | None = None, event: str | None = None
    ):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update(self, rover, movement: str | None = None, event: str | None = None):
        self.display(rover, movement, event)


class ConsoleDisplayer(Displayer):
    """
    The ConsoleDisplayer class provides a console-based display of the rover's position
    on the map. It clears the console and prints the map with the rover's current
    position and direction after each update.
    """

    def display(
        self, rover: Rover, movement: str | None = None, event: str | None = None
    ):
        system("clear")
        for y in range(self.map.height):
            row = ""
            for x in range(self.map.width):
                if x == rover.x and y == rover.y:
                    row += "🤖"
                elif self.map.matrix[y][x] == 1:
                    row += "🪨 "
                else:
                    row += "  "
            print(row)
        print(
            f"\nRover Position: ({rover.x:03d}, {rover.y:03d})   Direction: {rover.direction}   Movement: {movement}\n"
        )
        if event == "collision":
            print("⚠️  Collision avoided with an obstacle!")
        sleep(0.2)
