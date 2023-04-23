import os
from abc import ABC, abstractmethod
from typing import Optional
import pydicom
import nibabel as nib
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