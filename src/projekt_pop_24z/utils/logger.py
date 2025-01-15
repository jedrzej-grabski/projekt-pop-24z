from dataclasses import dataclass, field


@dataclass
class SwarmLogger:
    global_best_costs: list[float] = field(default_factory=list)
    iterations: int = 0

    def log_global_best_cost(self, best_cost: float) -> None:
        """Log the global best cost found by the swarm.

        Args:
            best_cost (float): The best cost found by the swarm.
        """
        self.global_best_costs.append(best_cost)
