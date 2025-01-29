from projekt_pop_24z.benchmark_functions.rosenbrock import Rosenbrock
from projekt_pop_24z.utils.plotter import PlotDescription
from src.projekt_pop_24z.benchmark import (
    run_benchmark_and_plot,
    pretty_print_result,
    AlgorithmParameters,
    LogParameters,
    run_benchmark_and_plot_aggregated,
)

from src.projekt_pop_24z.benchmark_functions.repository import (
    Sphere,
    Rosenbrock,
    Rastrigin,
)
from src.projekt_pop_24z.swarm.pso import Task
from src.projekt_pop_24z.utils.plotter import PlotType


EPSILON = 0.001
FUNCTION = Sphere

DYNAMIC_INERTIA = False
INERTIA_DECAY = 1.0002

DIMENSIONS = 2

SAVE_PATH = FUNCTION.name + ".png"


def main():

    bounds = [[-2.048, 2.048] for _ in range(DIMENSIONS)]

    parameters = AlgorithmParameters(
        swarm_size=20,
        bounds=bounds,
        dimensions=DIMENSIONS,
        task=Task.MINIMIZE,
        iterations=100,
        initial_inertia=0.8,
        cognitive_constant=2.0,
        social_constant=2.0,
        dynamic_inertia=DYNAMIC_INERTIA,
        inertia_decay=INERTIA_DECAY,
    )

    log_params = LogParameters(
        epsilon=EPSILON,
        name=FUNCTION.name,
        optimum_value=FUNCTION.optimum_value,
    )

    # result = run_benchmark_and_plot(
    #     cost_function=FUNCTION.function,
    #     parameters=parameters,
    #     log_params=log_params,
    #     plot_description=PlotDescription(
    #         problem_name=FUNCTION.name, save_path=SAVE_PATH
    #     ),
    #     plot_types=[PlotType.GLOBAL_BEST_COSTS, PlotType.STARTING_AND_ENDING_POSITIONS],
    # )

    result = run_benchmark_and_plot_aggregated(
        cost_function=FUNCTION.function,
        parameters=parameters,
        log_params=log_params,
        plot_description=PlotDescription(
            problem_name=FUNCTION.name, save_path=SAVE_PATH
        ),
        plot_types=[PlotType.GLOBAL_BEST_COSTS, PlotType.STARTING_AND_ENDING_POSITIONS],
        n_times=30,
    )

    pretty_print_result(result)


if __name__ == "__main__":
    main()
