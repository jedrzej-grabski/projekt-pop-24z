from dataclasses import field, dataclass
from src.projekt_pop_24z.benchmark_functions.benchmark_func import BenchmarkFunction
from typing import Callable, List
import math


def rastrigin_function(position: List[float]) -> float:
    A = 10  # Constant that defines the function's amplitude
    return A * len(position) + sum(
        [(x**2 - A * math.cos(2 * math.pi * x)) for x in position]
    )


@dataclass
class Rastrigin(BenchmarkFunction):
    name: str = field(init=False, default="Rastrigin")
    optimum_value: float = field(init=False, default=0)  # Minimum value of the function
    function: Callable[[List[float]], float] = field(default=rastrigin_function)
    dimensions: int = field(init=False, default=2)  # Defined for 2 dimensions
