from .rad_image import RadImage
import numpy as np
import os

class RadNumpyImage(RadImage):

    def __init__(self, file_path: str|None = None):
        """
        Initialize the RadNumpyImage class.

        :param file_path: The file path to the Numpy image file, defaults to None
        """
        super().__init__(file_path)

    def load(self) -> None:
        """
        Load the Numpy image from the file path using the numpy library.
        The image data is stored as a NumPy array in the image_data attribute.
        """
        if self.file_path is None:
            raise ValueError("No file path provided.")
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        self.image_data = np.load(self.file_path)

    def save(self, output_file_path: str) -> None:
        """
        Save the Numpy image to the output file path using the numpy library.

        :param output_file_path: The output file path to save the Numpy image
        """
        if self.image_data is None:
            raise ValueError("No image data to save.")

        np.save(output_file_path, self.image_data)