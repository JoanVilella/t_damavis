from collections import deque
from typing import List, Tuple

def get_neighbors(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = position
    neighbors = []
    # directions for up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for dx, dy in directions:
        neighbors.append((x + dx, y + dy))
    return neighbors

def is_valid_position(labyrinth: List[List[str]], visited: set, position: Tuple[int, int]) -> bool:
    x, y = position
    n, m = len(labyrinth), len(labyrinth[0])
    return 0 <= x < n and 0 <= y < m and position not in visited and labyrinth[x][y] == '.'

def solve_labyrinth(labyrinth: List[List[str]]) -> int:
    n, m = len(labyrinth), len(labyrinth[0])
    visited = set()
    queue = deque([((0, 0), 0)])  # store position and distance in the queue
    visited.add((0, 0))

    while queue:
        (current_position, dist) = queue.popleft()
        if current_position == (n - 1, m - 1):  # if reached goal
            return dist

        for neighbor in get_neighbors(current_position):
            if is_valid_position(labyrinth, visited, neighbor):
                queue.append((neighbor, dist + 1))
                visited.add(neighbor)

    return -1  # if no path found

if __name__ == "__main__":
    # Define the labyrinth
    labyrinth = [
        ['.', '.', '.', '#', '.', '.', '.'],
        ['#', '#', '.', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.', '#', '#'],
        ['.', '#', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '#', '.']
    ]
    
    # Use the function
    path_length = solve_labyrinth(labyrinth)
    
    if path_length == -1:
        print("No valid path found.")
    else:
        print(f"The shortest path length is {path_length}.")
