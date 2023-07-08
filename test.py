import unittest
from typing import List
from labyrinthSolverDef import Labyrinth
from labyrinthSolverDef import Orientation

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

class TestLabyrinth(unittest.TestCase):
    def test_solve_maze(self):
        test_cases = [
            (labyrinth_1, 11),
            (labyrinth_2, -1),
            (labyrinth_3, 2),
            (labyrinth_4, 16)
        ]

        for i, (maze_input, expected_result) in enumerate(test_cases):
            with self.subTest(i=i):
                labyrinth = Labyrinth(maze_input, start=(0, 1, Orientation.HORIZONTAL), goal=(len(maze_input)-1, len(maze_input[0])-1))
                result = labyrinth.solve()
                self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
