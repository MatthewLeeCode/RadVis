from .rad_image import RadImage
import nibabel as nib
import os
from typing import Optional
import numpy as np
nib.Nifti1Header.quaternion_threshold = -1e-06

class RadNiftiImage(RadImage):
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the RadNiftiImage class.

        :param file_path: The file path to the NIFTI image file, defaults to None
        """
        super().__init__(file_path)

    def load(self) -> None:
        """
        Load the NIFTI image from the file path using the nibabel library.
        The image data is stored as a NumPy array in the image_data attribute.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        self.data = nib.load(self.file_path)
        self.image_data = np.asanyarray(self.data.dataobj, dtype=np.float32)
        self.metadata = self.data.header

    def save(self, output_file_path: str) -> None:
        """
        Save the NIFTI image to the output file path using the nibabel library.

        :param output_file_path: The output file path to save the NIFTI image
        """
        if self.image_data is None:
            raise ValueError("No image data to save.")

        nifti_data = nib.Nifti1Image(self.image_data, affine=np.eye(4))
        nib.save(nifti_data, output_file_path)