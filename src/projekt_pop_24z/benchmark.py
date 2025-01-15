from pathlib import Path
from typing import Callable, Optional
from dataclasses import dataclass
from src.projekt_pop_24z.utils.logger import SwarmLogger
from projekt_pop_24z.swarm.pso import Coordinates, Bounds, Task, Swarm
from src.projekt_pop_24z.utils.plotter import PlotDescription, plot_global_best_costs


@dataclass
class AlgorithmParameters:
    swarm_size: int
    bounds: Bounds
    dimensions: int
    task: Task
    iterations: int
    initial_inertia: float
    cognitive_constant: float
    social_constant: float


@dataclass
class OptimizationResult:
    best_position: Coordinates
    best_cost: float


def run_single_benchmark(
    problem_name: str,
    cost_function: Callable[[Coordinates], float],
    parameters: AlgorithmParameters,
    logging: bool = False,
    visualize_plot: bool = False,
    save_plot: bool = False,
    save_path: Optional[Path] = None,
) -> OptimizationResult:

    logger = SwarmLogger() if logging else None

    swarm = Swarm(
        swarm_size=parameters.swarm_size,
        bounds=parameters.bounds,
        dimensions=parameters.dimensions,
        task=parameters.task,
        cost_function=cost_function,
        logger=logger,
    )

    swarm.init_swarm()

    optimization_result = swarm.run_optimization(
        iterations=parameters.iterations,
        initial_inertia=parameters.initial_inertia,
        cognitive_constant=parameters.cognitive_constant,
        social_constant=parameters.social_constant,
    )

    if visualize_plot or save_plot:
        if logger is not None:
            plot_description = PlotDescription(
                problem_name=problem_name, save_path=save_path
            )
            plot_global_best_costs(
                logger, plot_description, save=save_plot, show=visualize_plot
            )

        else:
            raise ValueError("Cannot visualize or save plot without logging")

    return OptimizationResult(
        best_position=optimization_result, best_cost=cost_function(optimization_result)
    )
