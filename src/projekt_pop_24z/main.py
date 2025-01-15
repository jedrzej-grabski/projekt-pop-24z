from pathlib import Path
from src.projekt_pop_24z.benchmark import run_single_benchmark, AlgorithmParameters
from src.projekt_pop_24z.benchmark_functions.sphere import sphere_function
from projekt_pop_24z.swarm.pso import Task

if __name__ == "__main__":
    dim = 5
    bounds_5d = [[-5.0, 5.0] for _ in range(dim)]

    parameters_5d = AlgorithmParameters(
        swarm_size=40,
        bounds=bounds_5d,
        dimensions=dim,
        task=Task.MINIMIZE,
        iterations=100,
        initial_inertia=0.7,
        cognitive_constant=2.0,
        social_constant=2.0,
    )

    result = run_single_benchmark(
        "Sphere function in 5 dimensions",
        sphere_function,
        parameters_5d,
        logging=True,
        save_plot=True,
        save_path=Path("sphere_5d.png"),
    )

    print(
        f"Best position: {[round(pos, 5) for pos in result.best_position]}\nBest cost: {round(result.best_cost, 5)}"
    )
