from dataclasses import dataclass, field
import math
from typing import Callable
import random
import enum


from src.projekt_pop_24z.utils.logger import SwarmLogger


Coordinates = list[float]
Bounds = list[Coordinates]


@dataclass
class Particle:
    dimensions: int
    position: Coordinates = field(default_factory=list)
    personal_best_position: Coordinates = field(default_factory=list)
    velocity: Coordinates = field(default_factory=list)

    def initialize_particle(self, bounds: list[Coordinates]) -> None:
        """Initialize the particle's position and velocity based on the bounds.

        Args:
            bounds (list[Coordinates]): Bounds for each dimension of the particle's position.
        """
        self.position = [random.uniform(*bound) for bound in bounds]
        self.personal_best_position = self.position
        self.velocity = [
            random.uniform(-abs(bound[1] - bound[0]), abs(bound[1] - bound[0]))
            for bound in bounds
        ]

    def update_velocity(
        self,
        global_best_position: Coordinates,
        inertia_coefficient: float,
        cognitive_constant: float,
        social_constant: float,
    ) -> None:
        """Update the velocity of the particle based on the standard PSO velocity equation.

        v(t+1) = w * v(t)
                + c1 * r1 * (p_best - x(t))
                + c2 * r2 * (g_best - x(t))

        Args:
            global_best_position (Coordinates): The overall best position found by the swarm.
            inertia_coefficient (float): Inertia weight (may be adjusted dynamically).
            cognitive_constant (float): Acceleration constant for the cognitive component.
            social_constant (float): Acceleration constant for the social component.
        """
        for d in range(self.dimensions):
            r1 = random.random()
            r2 = random.random()

            cognitive_velocity = (
                cognitive_constant
                * r1
                * (self.personal_best_position[d] - self.position[d])
            )
            social_velocity = (
                social_constant * r2 * (global_best_position[d] - self.position[d])
            )

            self.velocity[d] = (
                inertia_coefficient * self.velocity[d]
                + cognitive_velocity
                + social_velocity
            )


class Task(enum.Enum):
    MINIMIZE = enum.auto()
    MAXIMIZE = enum.auto()


@dataclass
class Swarm:
    swarm_size: int
    bounds: Bounds
    dimensions: int
    task: Task
    cost_function: Callable[[Coordinates], float]
    logger: SwarmLogger
    particles: list[Particle] = field(default_factory=list)
    global_best_position: Coordinates = field(default_factory=list)
    dynamic_inertia: bool = False
    inertia_decay: float = 0
    current_iteration: int = field(init=False, default=0)

    def __post_init__(self):
        if not self.dynamic_inertia and self.inertia_decay != 0:
            raise ValueError(
                "Inertia decay should be set only if dynamic_inertia is enabled."
            )

        if not (1.0001 <= self.inertia_decay <= 1.005) and self.dynamic_inertia:
            raise ValueError("Inertia decay should be in the range [1.0001, 1.005].")

    def init_swarm(self) -> None:
        for _ in range(self.swarm_size):
            particle = Particle(dimensions=self.dimensions)
            particle.initialize_particle(self.bounds)
            self.particles.append(particle)
        self.global_best_position = self.particles[0].position

    def update_global_best(self) -> Coordinates:
        """Find the global best position based on the particles' personal bests and the defined task.

        Returns:
            Coordinates: The global best position.
        """

        comparison_fn = max if self.task is Task.MAXIMIZE else min

        best_particle = comparison_fn(
            self.particles, key=lambda p: self.cost_function(p.personal_best_position)
        )

        return best_particle.personal_best_position[:]

    def update_inertia(self, initial_inertia: float) -> float:
        """Update the inertia coefficient based on the current iteration.

        The inertia coefficient is updated using the following formula:
        w' = w*u^(-k), where u is the strength of the decay and k is the current iteration.

        Args:
            initial_inertia (float): Initial inertia coefficient (w_start).

        Returns:
            float: Updated inertia coefficient.
        """

        new_inertia = initial_inertia * math.pow(
            self.inertia_decay, -self.current_iteration
        )

        return new_inertia

    def run_optimization(
        self,
        iterations: int,
        initial_inertia: float,
        cognitive_constant: float,
        social_constant: float,
    ) -> Coordinates:
        """Run the PSO algorithm for a specified number of iterations.

        Args:
            iterations (int): Number of iterations to run.
            initial_inertia (float): Starting inertia value (w).
            cognitive_constant (float): c1 (cognitive acceleration).
            social_constant (float): c2 (social acceleration).

        Returns:
            Coordinates: The best solution found by the swarm.
        """

        w = initial_inertia
        self.logger.add_inertia(w)

        if not self.particles:
            self.init_swarm()

        self.logger.add_particle_epoch([p.position for p in self.particles])

        self.global_best_position = self.update_global_best()

        initial_cost = self.cost_function(self.global_best_position)
        self.logger.log_global_best_cost(initial_cost)

        for _ in range(iterations):

            w = self.update_inertia(w) if self.dynamic_inertia else w

            for particle in self.particles:

                particle.update_velocity(
                    global_best_position=self.global_best_position,
                    inertia_coefficient=w,
                    cognitive_constant=cognitive_constant,
                    social_constant=social_constant,
                )

                self._update_particle_position(particle)

                current_cost = self.cost_function(particle.position)
                personal_best_cost = self.cost_function(particle.personal_best_position)

                better_condition = (
                    current_cost > personal_best_cost
                    if self.task is Task.MAXIMIZE
                    else current_cost < personal_best_cost
                )

                if better_condition:
                    particle.personal_best_position = particle.position[:]

            self.global_best_position = self.update_global_best()

            self.logger.log_global_best_cost(
                self.cost_function(self.global_best_position)
            )

            self.logger.add_inertia(w)
            self.logger.add_particle_epoch([p.position for p in self.particles])

            self.logger.increment_iterations()
            self.logger.check_epsilon()

            self.current_iteration += 1

        return self.global_best_position

    def _update_particle_position(self, particle: Particle) -> None:
        """Update particle's position based on its velocity, respecting bounds."""
        for d in range(self.dimensions):

            particle.position[d] += particle.velocity[d]

            lower_bound, upper_bound = self.bounds[d]
            if particle.position[d] < lower_bound:
                particle.position[d] = lower_bound
            elif particle.position[d] > upper_bound:
                particle.position[d] = upper_bound
