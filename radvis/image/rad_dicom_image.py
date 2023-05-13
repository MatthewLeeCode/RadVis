from .rad_image import RadImage
import pydicom
import os
from typing import Optional
import numpy as np


class RadDicomImage(RadImage):
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the RadDicomImage class.

        :param file_path: The file path to the DICOM image file, defaults to None
        """
        super().__init__(file_path)

    def load(self) -> None:
        """
        Load the DICOM image from the file path using the pydicom library.
        The image data is stored as a NumPy array in the image_data attribute.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        self.data = pydicom.dcmread(self.file_path)
        self.image_data = np.array(self.data.pixel_array, dtype=np.float32)
        self.metadata = self.data.file_meta

    def save(self, output_file_path: str) -> None:
        """
        Save the DICOM image to the output file path using the pydicom library.

        :param output_file_path: The output file path to save the DICOM image
        """
        if self.image_data is None:
            raise ValueError("No image data to save.")

        self.data.PixelData = self.image_data.tobytes()
        self.data.save_as(output_file_path)