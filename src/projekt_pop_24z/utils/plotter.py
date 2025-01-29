# type: ignore
from pathlib import Path
from typing import Optional, Callable, List
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from dataclasses import dataclass
from src.projekt_pop_24z.utils.logger import SwarmLogger
from matplotlib import cm
import numpy as np
from enum import Enum


class PlotType(Enum):
    GLOBAL_BEST_COSTS = "Global Best Costs"
    STARTING_AND_ENDING_POSITIONS = "Starting and Ending Positions"


@dataclass
class PlotDescription:
    problem_name: str
    save_path: str


@dataclass
class Plotter:
    logger: SwarmLogger
    plot_description: PlotDescription
    bounds: List[List[float]]
    func: Callable[[List[float]], float]

    def plot_starting_and_ending_positions_two_dimensional(self) -> None:
        """
        Plot the starting positions of particles in 2D with a contour plot background.

        Args:
            logger (SwarmLogger): Logger containing particle positions history.
            plot_description (PlotDescription): Plot description metadata.
            show (bool): Whether to show the plot.
            save (bool): Whether to save the plot.
            func (Callable[[float, float], float]): The function to plot as a contour background.
            resolution (int): Resolution of the grid for the contour plot.
        """
        # Get the starting particle positions
        particle_positions = self.logger.particle_positions_history[0]
        x = [pos[0] for pos in particle_positions]
        y = [pos[1] for pos in particle_positions]

        particle_final_positions = self.logger.particle_positions_history[-1]
        x_final = [pos[0] for pos in particle_final_positions]
        y_final = [pos[1] for pos in particle_final_positions]

        # Create a grid for the contour plot
        x_min, x_max = (
            min(x) + self.bounds[0][0] * 0.1,
            max(x) + self.bounds[1][1] * 0.1,
        )
        y_min, y_max = (
            min(y) + self.bounds[1][0] * 0.1,
            max(y) + self.bounds[0][1] * 0.1,
        )
        x_grid, y_grid = np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100)
        X, Y = np.meshgrid(x_grid, y_grid)

        # Compute the function values over the grid
        Z = np.array([[self.func([xi, yi]) for xi in x_grid] for yi in y_grid])

        # Plot the contour
        plt.contourf(X, Y, Z, levels=50, cmap="viridis", alpha=0.7)

        # Overlay the starting positions
        plt.scatter(x, y, s=6, color="red", label="Starting Positions")
        plt.scatter(x_final, y_final, s=6, color="blue", label="Ending Positions")

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(
            f"Start and finish points - {self.plot_description.problem_name}",
            loc="left",
        )

        # Move the legend outside the plot
        plt.legend(bbox_to_anchor=(1.05, 0.5), loc="upper left", borderaxespad=0.0)

        plt.savefig("start_end_" + self.plot_description.save_path, bbox_inches="tight")

        plt.clf()

    def plot_global_best_costs(self) -> None:

        inertia_history = self.logger.inertia_history
        global_best_costs = self.logger.global_best_costs
        iterations = range(len(global_best_costs))

        norm = Normalize(min(inertia_history), max(inertia_history))
        cmap = cm.get_cmap("viridis")  # Properly get the 'viridis' colormap
        colors = [cmap(norm(value)) for value in inertia_history]

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the line connecting the dots
        ax.plot(
            iterations,
            global_best_costs,
            color="gray",
            label="Global Best Cost (Trend)",
        )

        # Create scatter plot with gradient colors
        _ = ax.scatter(
            iterations,
            global_best_costs,
            c=colors,
            s=30,
            label="Global Best Cost (Points)",
        )

        # Add a colorbar to the figure and associate it with the scatter plot
        cbar = fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax)
        cbar.set_label("Inertia")

        # Standard plot settings
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Cost")
        ax.set_title(f"Global Best Costs - {self.plot_description.problem_name}")
        ax.legend()

        # Save the plot
        plt.savefig("global_best_" + self.plot_description.save_path)

        plt.clf()
