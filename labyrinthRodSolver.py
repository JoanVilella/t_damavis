from typing import List, Tuple
from collections import deque

# right, down, left, up, stay (for rotation)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
count_neighbors = 0


def can_rotate(maze: List[List[str]], position: Tuple[int, int, int]) -> bool:
    x, y, _ = position
    n, m = len(maze), len(maze[0])
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < n and 0 <= new_y < m) or maze[new_x][new_y] == '#':
                return False
    return True


def get_neighbors(maze: List[List[str]], position: Tuple[int, int, int], n: int, m: int) -> List[Tuple[int, int, int]]:
    x, y, o = position
    neighbors = []
    for dx, dy in directions:
        neighbors.append((x + dx, y + dy, o))
    # add rotation neighbor

    if can_rotate(maze, position):
        neighbors.append((x, y, 1 - o))
    return neighbors


def is_valid_position(maze: List[List[str]], visited: set, position: Tuple[int, int, int]) -> bool:
    x, y, o = position
    n, m = len(maze), len(maze[0])
    cells = [(x, y)]  # center cell
    if o == 0:  # horizontal
        cells.append((x, y - 1))  # left cell
        cells.append((x, y + 1))  # right cell
    else:  # vertical
        cells.append((x - 1, y))  # top cell
        cells.append((x + 1, y))  # bottom cell
    # check if all cells are valid and not walls
    for (cell_x, cell_y) in cells:
        if not (0 <= cell_x < n and 0 <= cell_y < m) or maze[cell_x][cell_y] == '#':
            return False
    # check if the center of the rod has been visited with the same orientation
    if position in visited:
        return False
    return True

def is_goal_reached(position: Tuple[int, int, int], n: int, m: int) -> bool:
    x, y, o = position
    cells = []
    if o == 0:  # horizontal
        cells.append((x, y - 1))
        cells.append((x, y + 1))
    else:  # vertical
        cells.append((x - 1, y))
        cells.append((x + 1, y))
    return any(cell == (n - 1, m - 1) for cell in cells)


def solve_maze(maze: List[List[str]]) -> int:
    n, m = len(maze), len(maze[0])
    visited = set()
    queue = deque([((0, 1, 0), 0)])  # store position and moves in the queue
    visited.add((0, 1, 0))

    while queue:
        (current_position, moves) = queue.popleft()

        # Check if any cell of the rod is at the goal
        if is_goal_reached(current_position, n, m):
            return moves

        for neighbor in get_neighbors(maze, current_position, n, m):
            if is_valid_position(maze, visited, neighbor):
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

    for i, (maze, expected_result) in enumerate(test_cases):
        result = solve_maze(maze)
        print(f"Test Case {i+1}: ", "Passed" if result == expected_result else "Failed", f"(got: {result}, expected: {expected_result})")

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
