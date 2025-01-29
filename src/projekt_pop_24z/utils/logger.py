from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class LogParameters:
    name: str
    optimum_value: float = 0
    epsilon: float = -1


@dataclass
class SwarmLogger:
    name: str
    epsilon: float
    optimum_position: float
    epsilon_reached: bool = field(init=False, default=False)
    global_best_costs: list[float] = field(default_factory=list)
    iterations: int = field(init=False, default=0)
    iterations_until_epsilon: int = field(init=False, default=-1)
    particle_positions_history: list[list[list[float]]] = field(default_factory=list)
    inertia_history: list[float] = field(default_factory=list)

    def log_global_best_cost(self, best_cost: float) -> None:
        """Log the global best cost found by the swarm.

        Args:
            best_cost (float): The best cost found by the swarm.
        """
        self.global_best_costs.append(best_cost)

    def increment_iterations(self) -> None:
        """Increment the number of iterations."""
        self.iterations += 1

    def check_epsilon(self) -> None:
        """Check if the epsilon condition is met."""
        if not self.epsilon_reached and self.epsilon > 0:
            if abs(self.global_best_costs[-1]) < self.epsilon:
                self.epsilon_reached = True
                self.iterations_until_epsilon = self.iterations

    def add_particle_epoch(self, particle_positions: list[list[float]]) -> None:
        """Add the particle positions to the history.

        Args:
            particle_positions (list[float]): List of particles positions.
        """
        self.particle_positions_history.append(deepcopy(particle_positions))

    def add_inertia(self, inertia: float) -> None:
        """Add the inertia value to the history.

        Args:
            inertia (float): The inertia value.
        """
        self.inertia_history.append(inertia)
