import pytest

from src.projekt_pop_24z.swarm.pso import Swarm, Particle, Task


def test_update_global_best_minimize():
    bounds = [[0, 10], [0, 10]]
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
    bounds = [[0, 10], [0, 10]]
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
