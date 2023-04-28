"""
Functions for plotting RadImages as slices.
"""
import matplotlib.pyplot as plt
from radvis.image.rad_image import RadImage


def plot_slice(radimage: RadImage, index: int, axis: int = 0, ax=None, 
               cmap='gray', **kwargs) -> plt.Axes:
    """ Plot a slice of a RadImage.

    :param radimage: RadImage to plot.
    :param index: Index of the slice to plot.
    :param axis: Axis along which to plot the slice.
    :param ax: Axes on which to plot the image. If None, a new figure and axes are created.
    :param cmap: Colormap to use for plotting.
    :param **kwargs: Additional keyword arguments are passed to matplotlib.axes.Axes.imshow.

    :return: Axes on which the image was plotted.
    """
    if ax is None:
        _, ax = plt.subplots()
    plt.imshow(radimage.get_slice(index, axis), cmap=cmap, **kwargs)
    return ax
