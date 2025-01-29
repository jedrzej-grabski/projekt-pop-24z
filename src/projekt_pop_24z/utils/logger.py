from __future__ import annotations
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

    @classmethod
    def aggregate(cls, loggers: list[SwarmLogger]) -> SwarmLogger:
        """Aggregate multiple loggers into one by averaging their values.

        Args:
            loggers (list[SwarmLogger]): List of loggers to aggregate.

        Returns:
            SwarmLogger: The aggregated logger.
        """
        if not loggers:
            raise ValueError("The loggers list should not be empty.")

        num_loggers = len(loggers)
        new_logger = deepcopy(loggers[0])

        # Average global best costs
        max_length = max(len(logger.global_best_costs) for logger in loggers)
        new_logger.global_best_costs = [
            sum(
                logger.global_best_costs[i]
                for logger in loggers
                if i < len(logger.global_best_costs)
            )
            / num_loggers
            for i in range(max_length)
        ]

        # Iterations remain the same
        new_logger.iterations = loggers[0].iterations

        # Average iterations until epsilon
        valid_iterations = [
            logger.iterations_until_epsilon
            for logger in loggers
            if logger.iterations_until_epsilon != -1
        ]
        new_logger.iterations_until_epsilon = int(
            sum(valid_iterations) / len(valid_iterations) if valid_iterations else -1
        )

        # Average particle positions history
        max_length = max(len(logger.particle_positions_history) for logger in loggers)
        new_logger.particle_positions_history = [
            [
                [
                    sum(
                        logger.particle_positions_history[i][j][k]
                        for logger in loggers
                        if i < len(logger.particle_positions_history)
                        and j < len(logger.particle_positions_history[i])
                        and k < len(logger.particle_positions_history[i][j])
                    )
                    / num_loggers
                    for k in range(len(loggers[0].particle_positions_history[0][0]))
                ]
                for j in range(len(loggers[0].particle_positions_history[0]))
            ]
            for i in range(max_length)
        ]

        # Average inertia history
        max_length = max(len(logger.inertia_history) for logger in loggers)
        new_logger.inertia_history = [
            sum(
                logger.inertia_history[i]
                for logger in loggers
                if i < len(logger.inertia_history)
            )
            / num_loggers
            for i in range(max_length)
        ]

        return new_logger

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
