from projekt_pop_24z.utils.plotter import PlotDescription
from src.projekt_pop_24z.benchmark import (
    pretty_print_result,
    AlgorithmParameters,
    LogParameters,
    run_benchmark_and_plot_aggregated,
    run_single_benchmark,
)

from src.projekt_pop_24z.benchmark_functions.repository import (
    Sphere,
    Rosenbrock,
    Rastrigin,
)
from src.projekt_pop_24z.swarm.pso import Task, InertiaParams, DynamicInertiaType
from src.projekt_pop_24z.utils.plotter import PlotType


# variables
DIMENSIONS = 2
FUNCTION = Sphere
DYNAMIC_INERTIA = DynamicInertiaType.ADAPTIVE
INERTIA_DECAY = 1.0001
INITIAL_INERTIA = 0.5
EPSILON = 10e-5

INERTIA_PARAMS = InertiaParams(inertia_decay=INERTIA_DECAY, min_inertia=0.2)

# constants
SAVE_PATH = FUNCTION.name + ".png"
SOCIAL_CONSTANT = 2.0
COGNITIVE_CONSTANT = 2.0
BOUNDS = [[-2.048, 2.048] for _ in range(DIMENSIONS)]
TASK = Task.MINIMIZE
ITERATIONS = 10000
SWARM_SIZE = 50


def main():

    bounds = [[-2.048, 2.048] for _ in range(DIMENSIONS)]

    parameters = AlgorithmParameters(
        swarm_size=20,
        bounds=bounds,
        dimensions=DIMENSIONS,
        task=Task.MINIMIZE,
        iterations=300,
        initial_inertia=0.8,
        cognitive_constant=2.0,
        social_constant=2.0,
        dynamic_inertia=DYNAMIC_INERTIA,
        inertia_params=INERTIA_PARAMS,
    )

    log_params = LogParameters(
        epsilon=EPSILON,
        name=FUNCTION.name,
        optimum_value=FUNCTION.optimum_value,
    )

    # result = run_benchmark_and_plot_aggregated(
    #     cost_function=FUNCTION.function,
    #     parameters=parameters,
    #     log_params=log_params,
    #     plot_description=PlotDescription(
    #         problem_name=FUNCTION.name, save_path=SAVE_PATH
    #     ),
    #     plot_types=[PlotType.GLOBAL_BEST_COSTS, PlotType.STARTING_AND_ENDING_POSITIONS],
    #     n_times=30,
    # )

    result, logger = run_single_benchmark(
        cost_function=FUNCTION.function,
        parameters=parameters,
        log_params=log_params,
    )

    # print(f"{result.best_cost:.4f}")
    # for inert in logger.inertia_history:
    #     print(f"{inert:.4f}")

    pretty_print_result(result)
    print(logger.inertia_history[-1])


if __name__ == "__main__":
    main()
