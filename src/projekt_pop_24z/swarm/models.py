from dataclasses import dataclass, field
from typing import Callable
import random
import enum


Coordinates = list[float]


@dataclass
class Particle:
    dimensions: int
    position: Coordinates = field(default_factory=list)
    personal_best_position: Coordinates = field(default_factory=list)
    velocity: Coordinates = field(default_factory=list)

    def initialize_particle(self, bounds: list[Coordinates]) -> None:
        self.position = [random.uniform(*bound) for bound in bounds]
        self.personal_best_position = self.position
        self.velocity = [
            random.uniform(-abs(bound[1] - bound[0]), abs(bound[1] - bound[0]))
            for bound in bounds
        ]

    def update_velocity


class Task(enum.Enum):
    MINIMIZE = enum.auto()
    MAXIMIZE = enum.auto()


@dataclass
class Swarm:
    swarm_size: int
    bounds: list[Coordinates]
    dimensions: int
    task: Task
    cost_function: Callable[[Coordinates], float]
    particles: list[Particle] = field(default_factory=list)
    global_best_position: Coordinates = field(default_factory=list)

    def init_swarm(self) -> None:
        for _ in range(self.swarm_size):
            particle = Particle(dimensions=self.dimensions)
            particle.initialize_particle(self.bounds)
            self.particles.append(particle)
        self.global_best_position = self.particles[0].position

    def update_global_best(self) -> Coordinates:
        """Generates the global best position based on the task.

        Returns:
            Coordinates: The global best position.
        """
        best = max if self.task is Task.MAXIMIZE else min
        return best([particle.personal_best_position for particle in self.particles])
