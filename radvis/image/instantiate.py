from .rad_image import RadImage
from .rad_dicom_image import RadDicomImage
from .rad_nifti_image import RadNiftiImage
from .rad_numpy_image import RadNumpyImage
import numpy as np
import os

def load_image(file_path: str) -> RadImage:
    """
    Infer the file format of the image and load it using the appropriate RadImage subclass.

    :param file_path: The file path to the image file
    :return: An instance of a RadImage subclass for the corresponding file format
    """
    if file_path.find(".dcm") != -1:
        return RadDicomImage(file_path)
    elif file_path.find(".nii") != -1:
        return RadNiftiImage(file_path)
    elif file_path.find(".npy") != -1:
        return RadNumpyImage(file_path)
    else:
        extension = os.path.splitext(file_path)[1]
        raise ValueError(f"Unsupported file format: {extension}")


def from_numpy(image_data: np.ndarray) -> RadImage:
    """
    Create a RadImage from a NumPy array.

    :param image_data: The NumPy array to create the RadImage from
    :return: An instance of a RadImage subclass for the corresponding file format
    """
    assert isinstance(image_data, np.ndarray)
    image = RadNumpyImage()
    image.set_image_data(image_data)
    return image