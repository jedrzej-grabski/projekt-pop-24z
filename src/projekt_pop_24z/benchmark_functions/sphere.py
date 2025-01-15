from typing import List


def sphere_function(position: List[float]) -> float:
    return sum(x**2 for x in position)
