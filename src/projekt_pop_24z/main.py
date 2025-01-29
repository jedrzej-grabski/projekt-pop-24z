from projekt_pop_24z.utils.plotter import PlotDescription
from src.projekt_pop_24z.benchmark import (
    run_benchmark_and_plot,
    pretty_print_result,
    AlgorithmParameters,
    LogParameters,
)
from src.projekt_pop_24z.benchmark_functions.sphere import Sphere
from src.projekt_pop_24z.swarm.pso import Task
from src.projekt_pop_24z.utils.plotter import PlotType


EPSILON = 0.001
OPTIMUM = Sphere.optimum_value
NAME = "Sphere"

DYNAMIC_INERTIA = True

DIMENSIONS = 2

SAVE_PATH = "sphere.png"


def main():

    bounds = [[-2.0, 2.0] for _ in range(DIMENSIONS)]

    parameters = AlgorithmParameters(
        swarm_size=200,
        bounds=bounds,
        dimensions=DIMENSIONS,
        task=Task.MINIMIZE,
        iterations=10,
        initial_inertia=0.4,
        cognitive_constant=2.0,
        social_constant=2.0,
    )

    log_params = LogParameters(
        epsilon=EPSILON,
        name=NAME,
        optimum_value=OPTIMUM,
    )

    result = run_benchmark_and_plot(
        cost_function=Sphere.function,
        parameters=parameters,
        log_params=log_params,
        plot_description=PlotDescription(problem_name=NAME, save_path=SAVE_PATH),
        plot_types=[PlotType.GLOBAL_BEST_COSTS, PlotType.STARTING_AND_ENDING_POSITIONS],
    )

    pretty_print_result(result)


if __name__ == "__main__":
    main()
