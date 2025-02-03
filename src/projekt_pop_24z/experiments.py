import time
from itertools import product, chain
from loguru import logger
from src.projekt_pop_24z.benchmark import (
    AlgorithmParameters,
    OptimizationResult,
    pretty_print_result,
    run_benchmark_and_plot_aggregated,
)
from src.projekt_pop_24z.utils.logger import LogParameters
from src.projekt_pop_24z.utils.plotter import PlotDescription, PlotType
from src.projekt_pop_24z.swarm.pso import DynamicInertiaType, InertiaParams, Task
from src.projekt_pop_24z.benchmark_functions.repository import (
    Sphere,
    Rosenbrock,
    Ackley,
    Rastrigin,
    CEC2017_F1,
    CEC2014_F1,
)
from src.projekt_pop_24z.benchmark_functions.sphere import Sphere

EPSILON = 10e-5
SOCIAL_CONSTANT = 2.0
COGNITIVE_CONSTANT = 2.0
TASK = Task.MINIMIZE
SWARM_SIZE = 50
INITIAL_INERTIA = 0.1


def all_param_combs():
    non_cec_funcs = (Sphere, Rosenbrock, Ackley, Rastrigin)
    non_cec_dims = (5, 10, 20)

    cec_funcs = (CEC2014_F1, CEC2017_F1)
    cec_dims = (10, 20)

    exp_u_vals = (1.0001, 1.0003, 1.0005)
    adaptive_bounds = ((0.95, 1.01), (0.99, 1.01), (0.99, 1.05))

    func_dim_combinations = chain(
        product(non_cec_funcs, non_cec_dims), product(cec_funcs, cec_dims)
    )

    exp_params = ((DynamicInertiaType.EXPONENTIAL, v) for v in exp_u_vals)
    linear_params = ((DynamicInertiaType.LINEAR, 0.01),)
    adaptive_params = (
        (DynamicInertiaType.ADAPTIVE, bounds) for bounds in adaptive_bounds
    )
    static_params = ((DynamicInertiaType.NONE, None),)

    all_inertia_combinations = chain(
        exp_params, linear_params, adaptive_params, static_params
    )

    return product(func_dim_combinations, all_inertia_combinations)


def main():
    all_params = all_param_combs()
    ALL_EXPERIMENTS = 128
    n_experiment = 0
    results = []
    start_time = time.time()

    result_path = "results_iterative.txt"
    with open(result_path, "w"):
        pass  # clear the file on every launch

    for (func, dim), (itype, inertia_param) in all_params:
        n_experiment += 1
        percent_complete = round(n_experiment / ALL_EXPERIMENTS, 2) * 100
        elapsed_time = time.time() - start_time
        logger.info(
            f"Running experiment {n_experiment}/{ALL_EXPERIMENTS} ({percent_complete}%) "
            f"on function {func.name} in {dim} dimensions. Inertia setting: {itype}. Time elapsed: {elapsed_time:.2f}s"
        )

        iters = 500
        bounds = [func.bounds for _ in range(dim)]
        plot_path = f"plots/global_best/{func.name}/{dim}/{itype}_{inertia_param}"
        min_inertia = inertia_param if itype is DynamicInertiaType.ADAPTIVE else 0.01
        inertia_decay = (
            inertia_param if itype is DynamicInertiaType.EXPONENTIAL else 1.0001
        )
        inertia_params = InertiaParams(inertia_decay, min_inertia)  # type: ignore
        log_params = LogParameters(
            epsilon=EPSILON, name=func.name, optimum_value=func.optimum_value
        )
        parameters = AlgorithmParameters(
            swarm_size=SWARM_SIZE,
            bounds=bounds,
            dimensions=dim,
            task=TASK,
            iterations=iters,
            initial_inertia=INITIAL_INERTIA,
            cognitive_constant=COGNITIVE_CONSTANT,
            social_constant=SOCIAL_CONSTANT,
            dynamic_inertia=itype,  # type: ignore
            inertia_params=inertia_params,
        )

        result = run_benchmark_and_plot_aggregated(
            cost_function=func.function,
            parameters=parameters,
            log_params=log_params,
            plot_description=PlotDescription(
                problem_name=func.name, save_path=plot_path
            ),
            plot_types=[PlotType.GLOBAL_BEST_COSTS],
            n_times=25 if func not in (CEC2017_F1, CEC2014_F1) else 10,
        )
        with open(result_path, "a") as f:
            pretty_print_result(result, f)

        results.append(result)
        save_results(results)


def save_results(results: list[OptimizationResult]):
    with open("results_full.txt", "w") as f:
        for result in results:
            pretty_print_result(result, f)


if __name__ == "__main__":
    main()
