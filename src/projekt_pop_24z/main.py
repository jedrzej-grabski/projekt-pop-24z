from projekt_pop_24z.utils.plotter import PlotDescription
from src.projekt_pop_24z.benchmark import (
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


# variables
DIMENSIONS = 10
FUNCTION = Rastrigin
DYNAMIC_INERTIA = True
INERTIA_DECAY = 1.0001
INITIAL_INERTIA = 0.1
EPSILON = 10e-5

# constants
SAVE_PATH = FUNCTION.name + ".png"
SOCIAL_CONSTANT = 2.0
COGNITIVE_CONSTANT = 2.0
BOUNDS = [[-2.048, 2.048] for _ in range(DIMENSIONS)]
TASK = Task.MINIMIZE
ITERATIONS = 300
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
        inertia_decay=INERTIA_DECAY,
    )

    log_params = LogParameters(
        epsilon=EPSILON,
        name=FUNCTION.name,
        optimum_value=FUNCTION.optimum_value,
    )

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
