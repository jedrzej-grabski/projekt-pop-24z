from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
from dataclasses import dataclass
from src.projekt_pop_24z.utils.logger import SwarmLogger


@dataclass
class PlotDescription:
    problem_name: str
    save_path: Optional[Path]


def plot_global_best_costs(
    logger: SwarmLogger,
    plot_description: PlotDescription,
    show: bool,
    save: bool,
) -> None:

    plt.plot(logger.global_best_costs, label="Global Best Cost")  # type: ignore
    plt.xlabel("Iteration")  # type: ignore
    plt.ylabel("Cost")  # type: ignore
    plt.title(f"Global Best Costs for {plot_description.problem_name}")  # type: ignore
    plt.legend()  # type: ignore
    if save:
        plt.savefig(plot_description.save_path)  # type: ignore
    if show:
        plt.show()  # type: ignore
