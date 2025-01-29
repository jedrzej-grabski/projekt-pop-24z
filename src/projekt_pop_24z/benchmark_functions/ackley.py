from dataclasses import dataclass, field
import math
from typing import Callable
from projekt_pop_24z.benchmark_functions.base import BenchmarkFunction


def ackley_function(position: list[float]) -> float:
    a = 20
    b = 0.2
    c = 2 * math.pi
    n = len(position)

    sum1 = sum(x**2 for x in position)
    sum2 = sum(math.cos(c * x) for x in position)

    term1 = -a * math.exp(-b * math.sqrt(sum1 / n))
    term2 = -math.exp(sum2 / n)

    return term1 + term2 + a + math.e


@dataclass
class Ackley(BenchmarkFunction):
    name: str = field(init=False, default="Ackley")
    optimum_value: float = field(init=False, default=0)
    function: Callable[[list[float]], float] = field(default=ackley_function)
