from dataclasses import field, dataclass
from projekt_pop_24z.benchmark_functions.base import BenchmarkFunction
from typing import Callable, List


def sphere_function(position: List[float]) -> float:
    return sum([x**2 for x in position])


@dataclass
class Sphere(BenchmarkFunction):
    name: str = field(init=False, default="Sphere")
    optimum_value: float = field(init=False, default=0)
    function: Callable[[List[float]], float] = field(default=sphere_function)
