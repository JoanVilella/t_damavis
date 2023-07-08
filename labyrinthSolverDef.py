from enum import Enum
from collections import deque
from typing import List, Tuple

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Labyrinth:
    # Right, down, left, up, stay (for rotation)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]

    def __init__(self, labyrinth: List[List[str]], start: Tuple[int, int, Orientation], goal: Tuple[int, int]):
        # Check if labyrinth size constraints are respected
        if not (3 <= len(labyrinth) <= 1000):
            raise ValueError("Invalid labyrinth height: Expected a value between 3 and 1000.")
        for row in labyrinth:
            if not (3 <= len(row) <= 1000):
                raise ValueError("Invalid labyrinth width: Expected a value between 3 and 1000.")
        # Initialize labyrinth
        self.labyrinth = labyrinth
        self.start = start
        self.goal = goal
        self.visited = set()
        self.n = len(labyrinth)
        self.m = len(labyrinth[0]) if self.n > 0 else 0

    def solve(self) -> int:
        # Initialize queue with start position and 0 moves
        queue = deque([(self.start, 0)])
        self.visited.add(self.start)

        while queue:
            (current_position, moves) = queue.popleft()

            # Check if any cell of the rod is at the goal
            if self.is_goal_reached(current_position):
                return moves

            # If goal is not reached, add valid neighbors to the queue
            for neighbor in self.get_neighbors(current_position):
                if self.is_valid_position(neighbor):
                    # increase moves count
                    queue.append((neighbor, moves + 1))
                    self.visited.add(neighbor)

        return -1  # if no path found

    # Check if the end cells of the rod are at the goal
    def is_goal_reached(self, position: Tuple[int, int, Orientation]) -> bool:
        x, y, o = position
        cells = []

        # Depending on the orientation of the rod, append cells to be checked
        if o == Orientation.HORIZONTAL:
            cells.append((x, y - 1))
            cells.append((x, y + 1))
        else:  # o == Orientation.VERTICAL
            cells.append((x - 1, y))
            cells.append((x + 1, y))
        # Return True if any of the cells match the goal position
        return any(cell == self.goal for cell in cells)

    # Method to get neighboring positions
    def get_neighbors(self, position: Tuple[int, int, Orientation]) -> List[Tuple[int, int, Orientation]]:
        x, y, o = position
        neighbors = []
        # Add all neighboring cells to the list
        for dx, dy in Labyrinth.directions:
            neighbors.append((x + dx, y + dy, o))

        # add rotation neighbor if possible
        if self.can_rotate(position):
            neighbors.append((x, y, Orientation((o.value + 1) % 2)))
        return neighbors

    # Check if the rod can rotate at the given position
    def can_rotate(self, position: Tuple[int, int, Orientation]) -> bool:
        x, y, _ = position
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = x + dx, y + dy
                if not (0 <= new_x < self.n and 0 <= new_y < self.m) or self.labyrinth[new_x][new_y] == '#':
                    return False
        return True

    def is_valid_position(self, position: Tuple[int, int, Orientation]) -> bool:
        x, y, o = position
        cells = [(x, y)]  # center cell
        if o == Orientation.HORIZONTAL:
            cells.append((x, y - 1))  # left cell
            cells.append((x, y + 1))  # right cell
        else:  # o == Orientation.VERTICAL
            cells.append((x - 1, y))  # top cell
            cells.append((x + 1, y))  # bottom cell

        # check if all cells are valid and not walls
        for (cell_x, cell_y) in cells:
            if not (0 <= cell_x < self.n and 0 <= cell_y < self.m) or self.labyrinth[cell_x][cell_y] == '#':
                return False

        # check if the center of the rod has been visited with the same orientation
        if position in self.visited:
            return False

        return True
