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
    CEC2014_F1,
)
from src.projekt_pop_24z.swarm.pso import Task, InertiaParams, DynamicInertiaType
from src.projekt_pop_24z.utils.plotter import PlotType


# variables
DIMENSIONS = 10
FUNCTION = CEC2014_F1
DYNAMIC_INERTIA = DynamicInertiaType.NONE
INERTIA_DECAY = 1.005
INITIAL_INERTIA = 0.6
EPSILON = 10e-5

INERTIA_PARAMS = InertiaParams(inertia_decay=INERTIA_DECAY, min_inertia=0.2)

# constants
SAVE_PATH = FUNCTION.name + ".png"
SOCIAL_CONSTANT = 2.0
COGNITIVE_CONSTANT = 2.0
BOUNDS = [[-2.048, 2.048] for _ in range(DIMENSIONS)]
TASK = Task.MINIMIZE
ITERATIONS = 3000
SWARM_SIZE = 100


def main():

    bounds = [[-100.0, 100.0] for _ in range(DIMENSIONS)]

    parameters = AlgorithmParameters(
        swarm_size=SWARM_SIZE,
        bounds=bounds,
        dimensions=DIMENSIONS,
        task=Task.MINIMIZE,
        iterations=ITERATIONS,
        initial_inertia=INITIAL_INERTIA,
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

    print(FUNCTION.optimum_value)

    result = run_benchmark_and_plot_aggregated(
        cost_function=FUNCTION.function,
        parameters=parameters,
        log_params=log_params,
        plot_description=PlotDescription(
            problem_name=FUNCTION.name, save_path=SAVE_PATH
        ),
        plot_types=[PlotType.GLOBAL_BEST_COSTS],
        n_times=1,
    )

    pretty_print_result(result)


if __name__ == "__main__":
    main()
