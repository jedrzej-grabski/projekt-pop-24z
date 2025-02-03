from dataclasses import dataclass, field
from typing import Callable, List
from opfunu.cec_based.cec2014 import F12014
from opfunu.cec_based.cec2017 import F12017
from src.projekt_pop_24z.benchmark_functions.base import BenchmarkFunction


def function_2014_F1(position: List[float]) -> float:
    return float(F12014(ndim=len(position)).evaluate(position))  # type: ignore


@dataclass
class CEC2014_F1(BenchmarkFunction):
    name: str = field(init=False, default="CEC2014_F1")
    optimum_value: float = field(init=False, default=F12014().f_global)
    function: Callable[[List[float]], float] = field(default=function_2014_F1)
    bounds = (-100, 100)


def function_2017_F1(position: List[float]) -> float:
    return float(F12017(ndim=len(position)).evaluate(position))  # type: ignore


@dataclass
class CEC2017_F1(BenchmarkFunction):
    name: str = field(init=False, default="CEC2017_F1")
    optimum_value: float = field(init=False, default=F12017().f_global)
    function: Callable[[List[float]], float] = field(default=function_2017_F1)
    bounds = (-100, 100)
