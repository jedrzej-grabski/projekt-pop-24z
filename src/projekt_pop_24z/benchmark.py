from __future__ import annotations
from io import TextIOWrapper
from typing import Callable
from dataclasses import dataclass

from tabulate import tabulate

from src.projekt_pop_24z.utils.logger import LogParameters
from src.projekt_pop_24z.swarm.pso import (
    Task,
    Swarm,
    SwarmLogger,
    DynamicInertiaType,
    InertiaParams,
)
from src.projekt_pop_24z.utils.plotter import PlotDescription, Plotter, PlotType


Bounds = list[tuple[float, float]]
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
    dynamic_inertia: DynamicInertiaType
    inertia_params: InertiaParams


@dataclass
class OptimizationResult:
    logger: SwarmLogger
    algorithm_parameters: AlgorithmParameters
    best_position: Coordinates
    best_cost: float

    @classmethod
    def aggregate(
        cls, aggregated_logger: SwarmLogger, results: list[OptimizationResult]
    ) -> OptimizationResult:
        # Aggregate the results by averaging the best positions and costs
        num_results = len(results)
        best_positions = [
            sum(result.best_position[i] for result in results) / num_results
            for i in range(len(results[0].best_position))
        ]

        best_costs = sum(result.best_cost for result in results) / num_results

        return cls(
            logger=aggregated_logger,
            algorithm_parameters=results[0].algorithm_parameters,
            best_position=best_positions,
            best_cost=best_costs,
        )


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
        inertia_params=parameters.inertia_params,
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


def run_benchmark_and_plot_aggregated(
    cost_function: Callable[[Coordinates], float],
    parameters: AlgorithmParameters,
    log_params: LogParameters,
    plot_description: PlotDescription,
    plot_types: list[PlotType],
    n_times: int,
) -> OptimizationResult:
    results: list[OptimizationResult] = []
    loggers: list[SwarmLogger] = []

    for _ in range(n_times):
        result, logger = run_single_benchmark(cost_function, parameters, log_params)
        loggers.append(logger)
        results.append(result)

    aggregated_logger = SwarmLogger.aggregate(loggers)
    aggregated_result = OptimizationResult.aggregate(aggregated_logger, results)

    plotter = Plotter(
        logger=aggregated_logger,
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

    return aggregated_result


def pretty_print_result(result: OptimizationResult, sink: TextIOWrapper) -> None:

    def _print(text):
        print(text, file=sink)

    _print("-" * 30)
    _print(f"Benchmark Result for Function: {result.logger.name}")
    _print("-" * 30)

    # Algorithm Parameters as a Table
    params = result.algorithm_parameters
    param_table: list[list[object]] = [
        ["Swarm Size", params.swarm_size],
        ["Dimensions", params.dimensions],
        ["Bounds for all dimensions", params.bounds[0]],
        ["Task", params.task.name],
        ["Iterations", params.iterations],
        ["Initial Inertia", params.initial_inertia],
        ["Cognitive Constant", params.cognitive_constant],
        ["Social Constant", params.social_constant],
        ["Dynamic Inertia", "Enabled" if params.dynamic_inertia else "Disabled"],
    ]

    if params.dynamic_inertia:
        param_table.append(["Inertia Decay", params.inertia_params.inertia_decay])

    _print("\nAlgorithm Parameters:")
    _print(tabulate(param_table, headers=["Parameter", "Value"], tablefmt="grid"))

    # Optimization Results
    _print("\nOptimization Results:")
    _print(f"- Best Position: {[round(pos, 5) for pos in result.best_position]}")
    _print(f"- Best Cost: {result.best_cost:.10f}")
    if result.logger.epsilon != -1:
        _print(f"- Epsilon: {result.logger.epsilon}")
        if result.logger.epsilon_reached:
            _print(
                f"- Iterations until epsilon: {result.logger.iterations_until_epsilon}"
            )
        else:
            _print("- Epsilon not reached.")
    _print("\n" + "=|=" * 30 + "\n")
