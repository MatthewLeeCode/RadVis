import copy
from matplotlib.animation import FuncAnimation, PillowWriter
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
                 width:int=4, height:int=4, show_slider:bool = True) -> None:
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
        self._show_slider = show_slider
        self._image_plot = None
        self._mask_plots = []
        self._masks = []
        self._ax = None
        self._cmap = cmap
        self._figsize = (width, height)
        self._notebook_environment = IPython.get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
        self._slider_coords = None
        
    @property
    def title(self):
        """
        Returns the title. If title is 'None' then returns the title 'Axis: {axis}'
        """
        if self._title is None:
            return f"Axis: {self.axis}"
        return self._title    

    @property
    def width(self):
        """
        Returns the width of the figure.
        """
        return self._figsize[0]
    
    @property
    def height(self):
        """
        Returns the height of the figure.
        """
        return self._figsize[1]
    
    @property
    def figsize(self):
        """
        Returns the figure size.
        """
        return self._figsize

    def remove_slider(self) -> None:
        """
        Remove the slider from the plot.
        """
        self._show_slider = False
        del self._slider
        self._slider = None
    
    def set_slider_coordinates(self, x:float, y:float, width:float, height:float) -> None:
        """
        Set the coordinates of the slider.

        :param x: The x-coordinate of the slider
        :param y: The y-coordinate of the slider
        :param width: The width of the slider
        :param height: The height of the slider
        """
        self._slider_coords = [x, y, width, height]
    
    def _update_image(self, val:int) -> None:
        """
        Update the image plot with the selected slice.

        :param val: The index of the slice to display
        """
        image_slice = int(val)
        self._image_plot.set_data(self.radimage.get_slice(image_slice, self.axis))
        for plot, (mask, _, _) in zip(self._mask_plots, self._masks):
            plot.set_data(mask[image_slice, :, :] if self.axis == 0 else
                          mask[:, image_slice, :] if self.axis == 1 else
                          mask[:, :, image_slice])
        self.fig.canvas.draw_idle()

    def _create_slider(self, ax: plt.Axes, initial_index: int = 0) -> Slider|None:
        """
        Create a slider for the given plt.Axes object.

        :param ax: The plt.Axes object to add the slider to
        :param initial_index: The initial slice index, defaults to 0
        :return: A slider object (either ipywidgets.IntSlider or matplotlib Slider) or None
        """
        if self._show_slider is False:
            return None
        
        if self._notebook_environment:
            slider = interact(lambda val: self._update_image(val), 
                              val=IntSlider(min=0, max=self.radimage.shape[self.axis]-1, step=1, value=initial_index, 
                                            description=f"{self.title}: Slice"))
        else:
            ax_position = ax.get_position()
            slider_width = ax_position.width - 0.2
            slider_height = 0.03
            slider_x = ax_position.x0 + 0.1
            slider_y = ax_position.y0 - 0.15
            
            if self._slider_coords is not None:
                slider_x, slider_y, slider_width, slider_height = self._slider_coords
                
            ax_slider = plt.axes([slider_x, slider_y, slider_width, slider_height])
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
        self._image_plot = ax.imshow(
            self.radimage.get_slice(initial_index, self.axis), 
            cmap=self._cmap,
            vmin=self.radimage.image_data.min(),
            vmax=self.radimage.image_data.max(),
            interpolation='none'
        )
        for mask, cmap, alpha in self._masks:
            mask_plot = ax.imshow(mask[initial_index, :, :] if self.axis == 0 else
                      mask[:, initial_index, :] if self.axis == 1 else
                      mask[:, :, initial_index],
                      cmap=cmap, interpolation='none', alpha=alpha,
                      vmin=0, vmax=1)
            self._mask_plots.append(mask_plot)
        self._slider = self._create_slider(ax, initial_index)


    def display(self, ax: plt.Axes = None, initial_index: int = 0, show_plot=True) -> None:
        """
        Display the RadSlicer plot with a slider to control the displayed slice.
        """
        if len(self.radimage.shape) != 3:
            raise ValueError("display method expects a 3D image")

        if ax is None:
            self.fig, self._ax = plt.subplots()
            plt.subplots_adjust(bottom=0.2)
        else:
            self._ax = ax
            self.fig = ax.get_figure()
               
        self._ax.set_title(self.title, y=1)
        self.fig.set_size_inches(self._figsize[0], self._figsize[1], forward=False)
        
        self._plot_image(self._ax, initial_index)
        
        if show_plot:
            plt.show()

    def add_mask(self, mask: np.ndarray | RadImage, color: str = 'red', alpha: float = 0.5):
        """
        Adds a mask to the RadSlicer.

        :param mask: A 3D array that matches the shape of the radimage
        :param color: The color of the mask
        :param alpha: The opacity of the mask
        """
        if not isinstance(mask, np.ndarray) and not isinstance(mask, RadImage):
            raise ValueError("Mask must be a numpy array or RadImage object")
        
        if isinstance(mask, RadImage):
            mask = mask.image_data
        
        if mask.shape != self.radimage.shape:
            raise ValueError("Mask shape must match image shape")

        cmap = ListedColormap([color])
        mask = ma.masked_where(mask == 0, mask)
        
        self._masks.append((mask, cmap, alpha))
    
    def save_animation(self, filepath: str, fps: int = 10) -> None:
        """
        Save an animation of all slices to a GIF file.

        :param filepath: The path to save the animation to
        :param fps: The frames per second for the animation, defaults to 10
        """
        # Ensure display has been called at least once
        if self._ax is None:
            self.display()

        # Create the animation
        anim = FuncAnimation(self.fig, self._update_image, frames=self.radimage.shape[self.axis], interval=1000//fps)

        try:
            anim.save(filepath, writer=PillowWriter(fps=fps))
        except Exception as e:
            print(f"Could not save the animation due to the following error: {e}")
            
    def copy(self):
        """
        Create a copy of the RadSlicer object.
        """
        return copy.deepcopy(self)
    