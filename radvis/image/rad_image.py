from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class RadImage(ABC):
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the RadImage base class.

        :param file_path: The file path to the image file, defaults to None
        """
        self.file_path = file_path
        self.data = None
        self.image_data: Optional[np.ndarray] = None
        self.metadata = None
        if self.file_path:
            self.load()

    @abstractmethod
    def load(self) -> None:
        """
        Load the image from the file path. This method should be implemented
        by subclasses to handle specific image formats.
        """
        pass

    @abstractmethod
    def save(self, output_file_path: str) -> None:
        """
        Save the image to the output file path. This method should be implemented
        by subclasses to handle specific image formats.

        :param output_file_path: The output file path to save the image
        """
        pass
    
    def get_image_info(self) -> str:
        """
        Return information about the image shape and header.
        """
        if self.image_data is None:
            return "Image data not loaded"

        # Get the shape of the image
        shape_str = f"Shape: {self.image_data.shape}"

        # Get the header information
        header_str = ""
        if self.metadata is not None:
            for key, value in self.metadata.items():
                header_str += f"{key}: {value}\n"

        return f"{shape_str}\n{header_str}"

    def get_slice(self, index: int, axis: int = 0) -> np.ndarray:
        """
        Get a 2D slice of the image data along the specified axis and index.

        :param index: The index of the slice to take
        :param axis: The axis along which to take the slice
        :return: A 2D slice of the image data
        """
        if self.image_data is None:
            raise ValueError("Image data not loaded")

        # Checks that axis is within the bounds of the image data
        if axis < 0 or axis >= len(self.image_data.shape):
            raise ValueError(f"Axis {axis} is out of bounds for image data of shape {self.image_data.shape}")
        
        # Checks that the index is within the bounds of the image data
        if index < 0 or index >= self.image_data.shape[axis]:
            raise ValueError(f"Index {index} is out of bounds for axis {axis}")
        
        # Swap the desired axis with the first axis
        data = np.swapaxes(self.image_data, 0, axis)

        # Select the slice along the first axis
        slice_2d = data[index]

        return slice_2d

    def __recv__(self) -> str:
        """
        Return a string representation of the image data.
        """
        return self.get_image_info()
    
    def __getitem__(self, value:list) -> np.ndarray:
        """
        Return the image data at the given index.
        """
        return self.image_data[value]