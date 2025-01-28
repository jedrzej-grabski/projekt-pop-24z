from src.projekt_pop_24z.swarm.pso import Swarm, Particle, Task
import pytest


def test_update_global_best_minimize():
    bounds = [[0.0, 10.0], [0.0, 10.0]]
    particles = [
        Particle(dimensions=2, personal_best_position=[2, 3]),
        Particle(dimensions=2, personal_best_position=[1, 1]),
        Particle(dimensions=2, personal_best_position=[5, 6]),
    ]

    swarm = Swarm(
        swarm_size=3,
        bounds=bounds,
        dimensions=2,
        task=Task.MINIMIZE,
        cost_function=sum,
        particles=particles,
    )

    global_best = swarm.update_global_best()
    assert global_best == [1, 1], f"Expected [1, 1], got {global_best}"


def test_update_global_best_maximize():
    bounds = [[0.0, 10.0], [0.0, 10.0]]
    particles = [
        Particle(dimensions=2, personal_best_position=[2, 3]),
        Particle(dimensions=2, personal_best_position=[1, 1]),
        Particle(dimensions=2, personal_best_position=[5, 6]),
    ]

    swarm = Swarm(
        swarm_size=3,
        bounds=bounds,
        dimensions=2,
        task=Task.MAXIMIZE,
        cost_function=sum,
        particles=particles,
    )

    global_best = swarm.update_global_best()
    assert global_best == [5, 6], f"Expected [5, 6], got {global_best}"


def test_current_iteration():
    bounds = [[0.0, 10.0], [0.0, 10.0]]

    swarm = Swarm(
        swarm_size=3,
        bounds=bounds,
        dimensions=2,
        task=Task.MAXIMIZE,
        cost_function=sum,
    )

    res = swarm.run_optimization(
        iterations=10, initial_inertia=0.7, cognitive_constant=2.0, social_constant=2.0
    )
    assert res == [10.0, 10.0], f"Expected [10.0, 10.0], got {res}"
    assert swarm.current_iteration == 10, f"Expected 10, got {swarm.current_iteration}"


def test_current_iteration_min():
    bounds = [[0.0, 10.0], [0.0, 10.0]]

    swarm = Swarm(
        swarm_size=3,
        bounds=bounds,
        dimensions=2,
        task=Task.MINIMIZE,
        cost_function=sum,
    )

    res = swarm.run_optimization(
        iterations=10, initial_inertia=0.7, cognitive_constant=2.0, social_constant=2.0
    )
    assert res == [0.0, 0.0], f"Expected [0.0, 0.0], got {res}"
    assert swarm.current_iteration == 10, f"Expected 10, got {swarm.current_iteration}"


def test_wrong_inertia_decay():
    bounds = [[0.0, 10.0], [0.0, 10.0]]

    with pytest.raises(ValueError):
        _ = Swarm(
            swarm_size=3,
            bounds=bounds,
            dimensions=2,
            task=Task.MINIMIZE,
            cost_function=sum,
            dynamic_inertia=True,
            inertia_decay=0.9,
        )


def test_inertia_decay_with_not_dynamic():

    bounds = [[0.0, 10.0], [0.0, 10.0]]

    with pytest.raises(ValueError):
        _ = Swarm(
            swarm_size=3,
            bounds=bounds,
            dimensions=2,
            task=Task.MINIMIZE,
            cost_function=sum,
            dynamic_inertia=False,
            inertia_decay=1.0002,
        )
