from dataclasses import field, dataclass
from projekt_pop_24z.benchmark_functions.base import BenchmarkFunction
from typing import Callable, List


def rosenbrock_function(position: List[float]) -> float:
    return sum(
        [
            100 * (position[i + 1] - position[i] ** 2) ** 2 + (1 - position[i]) ** 2
            for i in range(len(position) - 1)
        ]
    )


@dataclass
class Rosenbrock(BenchmarkFunction):
    name: str = field(init=False, default="Rosenbrock")
    optimum_value: float = field(init=False, default=0)
    function: Callable[[List[float]], float] = field(default=rosenbrock_function)
