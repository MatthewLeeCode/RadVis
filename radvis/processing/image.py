from radvis.image.rad_image import RadImage 
import numpy as np
from scipy.ndimage import gaussian_filter


def normalization(rad_image: RadImage, min_val:float, max_val:float) -> RadImage:
    """
    Perform intensity normalization on a given RadImage.
    
    :param rad_image: The RadImage object to be normalized.

    :return: The normalized RadImage object.

    :raises ValueError: If image data is not loaded.
    """
    new_rad_image = rad_image.copy()
    if new_rad_image.image_data is None:
        raise ValueError("Image data not loaded")

    # Normalize the image data
    new_rad_image.image_data = (new_rad_image.image_data - min_val) / (max_val - min_val)
    return new_rad_image

def noise_reduction(rad_image: RadImage, sigma: float) -> RadImage:
    """
    Reduce noise in a given RadImage using Gaussian filtering.
    
    :param rad_image: The RadImage object to be processed.
    :param sigma: Standard deviation for the Gaussian filter.

    :return: The RadImage object with reduced noise.

    :raises ValueError: If image data is not loaded.
    """
    new_rad_image = rad_image.copy()
    if new_rad_image.image_data is None:
        raise ValueError("Image data not loaded")

    new_rad_image.image_data = gaussian_filter(new_rad_image.image_data, sigma=sigma)
    return new_rad_image

def percentile_clipping(rad_image: RadImage, lower_percentile: float, upper_percentile: float) -> RadImage:
    """
    Perform percentile clipping on a given RadImage.
    
    :param rad_image: The RadImage object to be clipped.
    :param lower_percentile: The lower percentile for intensity clipping.
    :param upper_percentile: The upper percentile for intensity clipping.

    :return: The RadImage object with intensity values clipped within the specified percentiles.

    :raises ValueError: If image data is not loaded.
    """
    new_rad_image = rad_image.copy()
    if new_rad_image.image_data is None:
        raise ValueError("Image data not loaded")

    # Compute the lower and upper intensity values
    lower = np.percentile(new_rad_image.image_data, lower_percentile)
    upper = np.percentile(new_rad_image.image_data, upper_percentile)

    # Clip the image data
    new_rad_image.image_data = np.clip(new_rad_image.image_data, lower, upper)
    return new_rad_image


def add_padding(rad_image: RadImage, expected_shape: tuple) -> RadImage:
    """
    Adds padding to either side of the image to match the expected shape.

    :param rad_image: The RadImage object to be padded.
    :param expected_shape: The expected shape of the image.

    :return: The RadImage object with padding added.
    """
    new_rad_image = rad_image.copy()
    if new_rad_image.image_data is None:
        raise ValueError("Image data not loaded")

    # Compute the padding
    padding = np.subtract(expected_shape, new_rad_image.image_data.shape)
    padding = np.array([padding // 2, padding - padding // 2]).T

    # Pad the image data
    new_rad_image.image_data = np.pad(new_rad_image.image_data, padding, mode='constant')
    return new_rad_image