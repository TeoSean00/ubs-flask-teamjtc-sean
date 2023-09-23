from queue import PriorityQueue
from typing import Tuple


def heuristic(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> int:
    x1, y1 = cell1
    x2, y2 = cell2

    return abs(x1 - x2) + abs(y1 - y2)

# def a_star(maze: )