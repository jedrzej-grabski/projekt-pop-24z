from dataclasses import dataclass
from typing import List, Callable


@dataclass
class BenchmarkFunction:
    name: str
    function: Callable[[List[float]], float]
    optimum_value: float = 0
    dimensions: int = 0
