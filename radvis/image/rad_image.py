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

    @property
    def shape(self) -> tuple:
        """
        Return the shape of the image data.
        """
        if self.image_data is None:
            return None
        return self.image_data.shape

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

        # Slice along the appropriate axis
        slicer = [slice(None)] * self.image_data.ndim
        slicer[axis] = index
        return self.image_data[tuple(slicer)]
    
    def copy(self):
        """ 
        Return a copy of the image.
        """
        new_image = self.__class__(self.file_path)
        new_image.data = self.data
        new_image.image_data = np.copy(self.image_data)
        new_image.metadata = self.metadata.copy() if self.metadata else None
        return new_image

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