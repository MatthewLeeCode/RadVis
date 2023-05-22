from radvis.visualize.rad_slicer import RadSlicer
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class RadSlicerGroup:
    def __init__(self, radslicers: list[RadSlicer], rows: int, cols: int) -> None:
        """
        Initialize the RadSlicerGroup class.

        :param radslicers: A list of RadSlicer objects
        :param rows: The number of rows to display the RadSlicers in
        :param cols: The number of columns to display the RadSlicers in
        """
        self.radslicers = radslicers
        self.rows = rows
        self.cols = cols
        self._verify_dimensions()

    def _verify_dimensions(self) -> None:
        """
        Verifies the provided rows and columns are valid for the number of RadSlicers.
        """
        if self.rows * self.cols != len(self.radslicers):
            raise ValueError(f"Number of RadSlicers ({len(self.radslicers)}) does not match provided grid dimensions ({self.rows}x{self.cols}).")

    def _get_figure_width(self) -> int:
        """
        Returns the width of the figure.
        """
        return self.cols * sum([rs.width for rs in self.radslicers])
    
    def _get_figure_height(self) -> int:
        """
        Returns the height of the figure.
        """
        return self.rows * sum([rs.height for rs in self.radslicers])
    
    def display(self, initial_index: int = 0) -> None:
        """
        Display the RadSlicers in a grid.
        """
        fig, axes = plt.subplots(self.rows, self.cols, figsize=(self._get_figure_width(), self._get_figure_height()))
        axes = axes.flatten()

        for i, (radslicer, ax) in enumerate(zip(self.radslicers, axes)):
            radslicer.display(ax=ax, initial_index=initial_index, show_plot=False)

        plt.tight_layout()
        plt.show()
