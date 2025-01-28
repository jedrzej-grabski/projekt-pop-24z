from typing import Callable
from dataclasses import dataclass

from tabulate import tabulate

from src.projekt_pop_24z.utils.logger import LogParameters
from src.projekt_pop_24z.swarm.pso import Task, Swarm, SwarmLogger
from src.projekt_pop_24z.utils.plotter import PlotDescription, Plotter, PlotType


Bounds = list[list[float]]
Coordinates = list[float]


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
    dynamic_inertia: bool = False
    inertia_decay: float = 0


@dataclass
class OptimizationResult:
    logger: SwarmLogger
    algorithm_parameters: AlgorithmParameters
    best_position: Coordinates
    best_cost: float


def run_single_benchmark(
    cost_function: Callable[[Coordinates], float],
    parameters: AlgorithmParameters,
    log_params: LogParameters,
) -> tuple[OptimizationResult, SwarmLogger]:

    logger = SwarmLogger(
        epsilon=log_params.epsilon,
        name=log_params.name,
        optimum_position=log_params.optimum_value,
    )

    swarm = Swarm(
        swarm_size=parameters.swarm_size,
        bounds=parameters.bounds,
        dimensions=parameters.dimensions,
        task=parameters.task,
        cost_function=cost_function,
        logger=logger,
        dynamic_inertia=parameters.dynamic_inertia,
        inertia_decay=parameters.inertia_decay,
    )

    swarm.init_swarm()

    optimization_result = swarm.run_optimization(
        iterations=parameters.iterations,
        initial_inertia=parameters.initial_inertia,
        cognitive_constant=parameters.cognitive_constant,
        social_constant=parameters.social_constant,
    )

    return (
        OptimizationResult(
            logger=logger,
            algorithm_parameters=parameters,
            best_position=optimization_result,
            best_cost=cost_function(optimization_result),
        ),
        logger,
    )


def run_benchmark_and_plot(
    cost_function: Callable[[Coordinates], float],
    parameters: AlgorithmParameters,
    log_params: LogParameters,
    plot_description: PlotDescription,
    plot_types: list[PlotType],
) -> OptimizationResult:
    result, logger = run_single_benchmark(cost_function, parameters, log_params)
    plotter = Plotter(
        logger=logger,
        plot_description=plot_description,
        bounds=parameters.bounds,
        func=cost_function,
    )

    for plot_type in plot_types:
        match plot_type:
            case PlotType.GLOBAL_BEST_COSTS:
                plotter.plot_global_best_costs()
            case PlotType.STARTING_AND_ENDING_POSITIONS:
                if parameters.dimensions != 2:
                    raise ValueError(
                        "Starting and ending positions plot is only supported for 2D problems."
                    )
                plotter.plot_starting_and_ending_positions_two_dimensional()

    return result


def pretty_print_result(result: OptimizationResult) -> None:
    print("-" * 30)
    print(f"Benchmark Result for Function: {result.logger.name}")
    print("-" * 30)

    # Algorithm Parameters as a Table
    params = result.algorithm_parameters
    param_table: list[list[object]] = [
        ["Swarm Size", params.swarm_size],
        ["Dimensions", params.dimensions],
        ["Bounds", params.bounds],
        ["Task", params.task.name],
        ["Iterations", params.iterations],
        ["Initial Inertia", params.initial_inertia],
        ["Cognitive Constant", params.cognitive_constant],
        ["Social Constant", params.social_constant],
        ["Dynamic Inertia", "Enabled" if params.dynamic_inertia else "Disabled"],
    ]

    if params.dynamic_inertia:
        param_table.append(["Inertia Decay", params.inertia_decay])

    print("\nAlgorithm Parameters:")
    print(tabulate(param_table, headers=["Parameter", "Value"], tablefmt="grid"))

    # Optimization Results
    print("\nOptimization Results:")
    print(f"- Best Position: {[round(pos, 9) for pos in result.best_position]}")
    print(f"- Best Cost: {result.best_cost:.10f}")
    if result.logger.epsilon != -1:
        print(f"- Epsilon: {result.logger.epsilon}")
        if result.logger.epsilon_reached:
            print(
                f"- Iterations until epsilon: {result.logger.iterations_until_epsilon}"
            )
        else:
            print("- Epsilon not reached.")
    print("\n" + "=|=" * 30 + "\n")
