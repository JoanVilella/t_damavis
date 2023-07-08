from typing import List, Tuple, NamedTuple
from collections import deque
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


# right, down, left, up, stay (for rotation)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]


class Position(NamedTuple):
    x: int
    y: int
    o: Orientation


# Define start and goal positions
START_POSITION = (0, 1, Orientation.HORIZONTAL)
GOAL_POSITION = None  # Will be set once the labyrinth is read


def can_rotate(labyrinth: List[List[str]], position: Position) -> bool:
    x, y, _ = position
    n, m = len(labyrinth), len(labyrinth[0])
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < n and 0 <= new_y < m) or labyrinth[new_x][new_y] == '#':
                return False
    return True


def get_neighbors(labyrinth: List[List[str]], position: Position, n: int, m: int) -> List[Position]:
    x, y, o = position
    neighbors = []
    for dx, dy in directions:
        neighbors.append(Position(x + dx, y + dy, o))
    # add rotation neighbor
    if can_rotate(labyrinth, position):
        neighbors.append(Position(x, y, Orientation((o.value + 1) % 2)))
    return neighbors


def is_valid_position(labyrinth: List[List[str]], visited: set, position: Position) -> bool:
    x, y, o = position
    n, m = len(labyrinth), len(labyrinth[0])
    cells = [(x, y)]  # center cell
    if o == Orientation.HORIZONTAL:
        cells.append((x, y - 1))  # left cell
        cells.append((x, y + 1))  # right cell
    else:  # vertical
        cells.append((x - 1, y))  # top cell
        cells.append((x + 1, y))  # bottom cell
    # check if all cells are valid and not walls
    for (cell_x, cell_y) in cells:
        if not (0 <= cell_x < n and 0 <= cell_y < m) or labyrinth[cell_x][cell_y] == '#':
            return False
    # check if the center of the rod has been visited with the same orientation
    if position in visited:
        return False
    return True


def is_goal_reached(position: Position, n: int, m: int) -> bool:
    x, y, o = position
    cells = []
    if o == Orientation.HORIZONTAL:
        cells.append((x, y - 1))
        cells.append((x, y + 1))
    else:  # vertical
        cells.append((x - 1, y))
        cells.append((x + 1, y))
    return any(cell == GOAL_POSITION for cell in cells)


def solve_labyrinth(labyrinth: List[List[str]]) -> int:
    global GOAL_POSITION
    n, m = len(labyrinth), len(labyrinth[0])
    GOAL_POSITION = (n - 1, m - 1)
    visited = set()
    # store position and moves in the queue
    queue = deque([(START_POSITION, 0)])
    visited.add(START_POSITION)

    while queue:
        (current_position, moves) = queue.popleft()

        # Check if any cell of the rod is at the goal
        if is_goal_reached(current_position, n, m):
            return moves

        for neighbor in get_neighbors(labyrinth, current_position, n, m):
            if is_valid_position(labyrinth, visited, neighbor):
                # increase moves count if orientation changeds
                queue.append((neighbor, moves + 1))
                visited.add(neighbor)

    return -1  # if no path found

# testing the code


def run_tests():
    test_cases = [
        (labyrinth_1, 11),
        (labyrinth_2, -1),
        (labyrinth_3, 2),
        (labyrinth_4, 16)
    ]

    for i, (labyrinth, expected_result) in enumerate(test_cases):
        result = solve_labyrinth(labyrinth)
        print(f"Test Case {i+1}: ", "Passed" if result == expected_result else "Failed",
              f"(got: {result}, expected: {expected_result})")


labyrinth_1 = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
               ["#", ".", ".", ".", "#", ".", ".", ".", "."],
               [".", ".", ".", ".", "#", ".", ".", ".", "."],
               [".", "#", ".", ".", ".", ".", ".", "#", "."],
               [".", "#", ".", ".", ".", ".", ".", "#", "."]]

labyrinth_2 = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
               ["#", ".", ".", ".", "#", ".", ".", "#", "."],
               [".", ".", ".", ".", "#", ".", ".", ".", "."],
               [".", "#", ".", ".", ".", ".", ".", "#", "."],
               [".", "#", ".", ".", ".", ".", ".", "#", "."]]

labyrinth_3 = [[".", ".", "."],
               [".", ".", "."],
               [".", ".", "."]]

labyrinth_4 = [[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", "#", ".", ".", ".", ".", "#", ".", ".", "."],
               [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", "#", ".", ".", ".", "#", ".", ".", ".", "."],
               [".", ".", ".", ".", ".", ".", "#", ".", ".", "."],
               [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
               [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]

if __name__ == "__main__":
    run_tests()
