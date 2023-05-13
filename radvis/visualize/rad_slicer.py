from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from radvis.image.rad_image import RadImage
import numpy as np
import numpy.ma as ma
import IPython
from ipywidgets import interact, IntSlider, Layout


class RadSlicer:
    def __init__(self, radimage: RadImage, axis: int = 0, title=None, cmap: str = "gray",
                 width=4, height=4) -> None:
        """
        Initialize the RadSlicer class.

        :param radimage: A RadImage object containing the image data
        :param axis: The image axis to slice along, defaults to 0
        :param cmap: The colormap to use for displaying the image, defaults to "gray"
        """
        self.radimage = radimage
        self.axis = axis
        self._title = title
        self._slider = None
        self._image_plot = None
        self._mask_plots = []
        self._masks = []
        self._ax = None
        self._cmap = cmap
        self._figsize = (width, height)
        self._notebook_environment = IPython.get_ipython().__class__.__name__ == 'ZMQInteractiveShell'

    @property
    def title(self):
        """
        Returns the title. If title is 'None' then returns the title 'Axis: {axis}'
        """
        if self._title is None:
            return f"Axis: {self.axis}"
        return self._title    

    def _update_image(self, val:int) -> None:
        """
        Update the image plot with the selected slice.

        :param val: The index of the slice to display
        """
        image_slice = int(val)
        self._image_plot.set_data(self.radimage.get_slice(image_slice, self.axis))
        for plot, (mask, cmap, alpha) in zip(self._mask_plots, self._masks):
            plot.set_data(mask[image_slice, :, :] if self.axis == 0 else
                          mask[:, image_slice, :] if self.axis == 1 else
                          mask[:, :, image_slice])
        self.fig.canvas.draw_idle()

    def _create_slider(self, ax: plt.Axes, initial_index: int = 0) -> Slider:
        """
        Create a slider for the given plt.Axes object.

        :param ax: The plt.Axes object to add the slider to
        :param initial_index: The initial slice index, defaults to 0
        :return: A slider object (either ipywidgets.IntSlider or matplotlib Slider)
        """
        if self._notebook_environment:
            slider = interact(lambda val: self._update_image(val), 
                              val=IntSlider(min=0, max=self.radimage.shape[self.axis]-1, step=1, value=initial_index, 
                                            description=f"{self.title}: Slice"))
        else:
            ax_position = ax.get_position()
            slider_width = ax_position.width - 0.2
            slider_x = ax_position.x0 + 0.1
            slider_y = ax_position.y0 - 0.15

            ax_slider = plt.axes([slider_x, slider_y, slider_width, 0.03])
            slider = Slider(ax_slider, f"Slice", 0, self.radimage.shape[self.axis] - 1, valstep=1, valfmt="%d",
                                valinit=initial_index)
            slider.on_changed(self._update_image)
        return slider
    
    def _plot_image(self, ax: plt.Axes, initial_index: int = 0) -> None:
        """
        Plot the image on the given plt.Axes object and create a slider for it.

        :param ax: The plt.Axes object to plot the image on
        :param initial_index: The initial slice index, defaults to 0
        """
        self._image_plot = ax.imshow(self.radimage.get_slice(initial_index, self.axis), cmap=self._cmap)
        for mask, cmap, alpha in self._masks:
            mask_plot = ax.imshow(mask[initial_index, :, :] if self.axis == 0 else
                      mask[:, initial_index, :] if self.axis == 1 else
                      mask[:, :, initial_index],
                      cmap=cmap, interpolation='none', alpha=alpha)
            self._mask_plots.append(mask_plot)
        self._slider = self._create_slider(ax, initial_index)


    def display(self, ax: plt.Axes = None, initial_index: int = 0) -> None:
        """
        Display the RadSlicer plot with a slider to control the displayed slice.
        """
        if len(self.radimage.shape) != 3:
            raise ValueError("display method expects a 3D image")

        if ax is None:
            self.fig, self._ax = plt.subplots()
            plt.subplots_adjust(bottom=0.2)
            
        self._ax.set_title(self.title, y=1)
        self.fig.set_size_inches(self._figsize[0], self._figsize[1], forward=False)
        
        self._plot_image(self._ax)
        plt.show()

    def add_mask(self, mask, color='red', alpha=0.5):
        """
        Adds a mask to the RadSlicer.

        :param mask: A 3D array that matches the shape of the radimage
        :param color: The color of the mask
        :param alpha: The opacity of the mask
        """
        if mask.shape != self.radimage.shape:
            raise ValueError("Mask shape must match image shape")

        # Create a custom colormap
        #cmap = ListedColormap(['none', color])
        cmap = ListedColormap([color])

        # Use numpy masked array to mask the '0' values
        mask = ma.masked_where(mask == 0, mask)
        
        self._masks.append((mask, cmap, alpha))