from dataclasses import dataclass
from typing import List, Callable


@dataclass
class BenchmarkFunction:
    name: str
    function: Callable[[List[float]], float]
    optimum_value: float = 0
    bounds: tuple[float, float] = (-2.048, 2.048)
